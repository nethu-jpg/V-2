#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex

from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

import re
import pyrogram

from pyrogram import (
    filters,
    Client
)

from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Message,
    CallbackQuery,
)

from bot import Bot
from script import script
from database.mdb import searchquery
from plugins.channel import deleteallfilters
from config import AUTH_USERS, IMDB_TEXT
from Omdb import get_posters

BUTTONS = {}

@Client.on_message(filters.group & filters.text)
async def filter(client: Bot, message: Message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if 2 < len(message.text) < 100:    
        btn = []

        group_id = message.chat.id
        name = message.text

        filenames, links = await searchquery(group_id, name)
        if filenames and links:
            for filename, link in zip(filenames, links):
                btn.append(
                    [InlineKeyboardButton(text=f"๐๐ผ {filename}",url=f"{link}")]
            )
           
        else:
            return

        if not btn:
            return

        if len(btn) > 6: 
            btns = list(split_list(btn, 6)) 
            keyword = f"๐๐ผ {message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton("โ แแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซ โ", url="https://t.me/Movie_Zone_KP/3")]
            )
            buttons.append(
                [InlineKeyboardButton(text="๐ฐ ๐ฃ๐๐๐  1/1 ๐ฐ",callback_data="pages")]
            )
            buttons.append(
                [InlineKeyboardButton("๐๐ป ๐๐๐ ๐๐๐ซ๐ข๐๐ฌ ๐๐๐ฆ๐๐๐ซ แแแบแแแบ ๐๐ป", url="https://t.me/Kpautoreply_bot")]
            )
            
            imdb=await get_posters(name)
            if imdb:
                cap = IMDB_TEXT.format(un=message.from_user.username, user=message.from_user.first_name, query=name, title=imdb['title'], trailer=imdb["trailer"], runtime=imdb["runtime"], languages=imdb["languages"], genres=imdb['genres'], year=imdb['year'], rating=imdb['rating'], url=imdb['url'])                                                  
            else:
                cap = f"<b>๐๐ผ แแญแฏแแบแธ  [{message.from_user.first_name}]({message.from_user.username}) แแฑ.... ๐๐\n\n[{message.from_user.first_name}]({message.from_user.username}) แแพแฌแแฌ ๐๐ป {message.text}๐๐ป  แแญแฏ แแแบแแแบแแฎแแพแแพแญแแฌ แแผแแฑแธแแฌแธแแแบแแฑแฌแบแโฅ๏ธ๐...\n\n<b>๐๐ผ Request by : [{message.from_user.first_name}]({message.from_user.username})</b>\n\n<b>โ๏ธ Join Main Channel \nโ๏ธ K-Series  ๐๐ป @MKSVIPLINK \nโ๏ธ Movie      ๐๐ป @KPMOVIELIST</b>\n</b>โ๏ธ ๐๐ฅ๐ก๐ค๐๐๐๐ ๐ฝ๐ฎ   : ๐๐ค ๐๐๐๐ฃ๐ ๐๐๐ฎ ๐ฅฐ</a>"    

            if imdb and imdb.get('poster'):
                try:                   
                    await message.reply_photo(photo=imdb.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md")                               
                except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                    pic = imdb.get('poster')
                    poster = pic.replace('.jpg', "._V1_UX360.jpg")
                    await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md")
                except Exception as e:
                    logger.exception(e)
                    await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md") 
            else: 
                await message.reply_text(
                    text=f"๐๐ผ แแญแฏแแบแธ  [{message.from_user.first_name}]({message.from_user.username}) แแฑ.... ๐๐\n\n[{message.from_user.first_name}]({message.from_user.username}) แแพแฌแแฌ ๐๐ป {message.text}๐๐ป  แแญแฏ แแแบแแแบแแฎแแพแแพแญแแฌ แแผแแฑแธแแฌแธแแแบแแฑแฌแบแโฅ๏ธ๐...\n\n๐๐ผ Request by : [{message.from_user.first_name}]({message.from_user.username})\n\nโ๏ธ Join Main Channel \nโ๏ธ K-Series  ๐๐ป @MKSVIPLINK \nโ๏ธ Movie      ๐๐ป @KPMOVIELIST\nโ๏ธ ๐๐ฅ๐ก๐ค๐๐๐๐ ๐ฝ๐ฎ   : ๐๐ค ๐๐๐๐ฃ๐ ๐๐๐ฎ ๐ฅฐ",         
                    reply_markup=InlineKeyboardMarkup(buttons),
                    parse_mode="md"
                )
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton("โ แแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซ โ", url="https://t.me/Movie_Zone_KP/3")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"๐ฐ ๐ฃ๐๐๐ 1/{data['total']} ๐ฐ",callback_data="pages"),InlineKeyboardButton(text="๐๐๐ฑ๐ญ ๐๐๐?๐ โฉ",callback_data=f"next_0_{keyword}")]
        )
        buttons.append(
            [InlineKeyboardButton("๐๐ป ๐๐๐ ๐๐๐ซ๐ข๐๐ฌ ๐๐๐ฆ๐๐๐ซ แแแบแแแบ ๐", url="https://t.me/Kpautoreply_bot")]
        )
        
        imdb=await get_posters(name)
        if imdb:
            cap = IMDB_TEXT.format(un=message.from_user.username, user=message.from_user.first_name, query=name, title=imdb['title'], trailer=imdb["trailer"], runtime=imdb["runtime"], languages=imdb["languages"], genres=imdb['genres'], year=imdb['year'], rating=imdb['rating'], url=imdb['url'])                                                  
        else:
            cap = f"<b>๐๐ผ แแญแฏแแบแธ  [{message.from_user.first_name}]({message.from_user.username}) แแฑ.... ๐๐\n\n[{message.from_user.first_name}]({message.from_user.username}) แแพแฌแแฌ ๐๐ป {message.text}๐๐ป  แแญแฏ แแแบแแแบแแฎแแพแแพแญแแฌ แแผแแฑแธแแฌแธแแแบแแฑแฌแบแโฅ๏ธ๐...\n\n<b>๐๐ผ Request by : [{message.from_user.first_name}]({message.from_user.username})</b>\n\n<b>โ๏ธ Join Main Channel \nโ๏ธ K-Series  ๐๐ป @MKSVIPLINK \nโ๏ธ Movie      ๐๐ป @KPMOVIELIST</b>\n</b>โ๏ธ ๐๐ฅ๐ก๐ค๐๐๐๐ ๐ฝ๐ฎ   : ๐๐ค ๐๐๐๐ฃ๐ ๐๐๐ฎ ๐ฅฐ</a>"    

        if imdb and imdb.get('poster'):
            try:                   
                await message.reply_photo(photo=imdb.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md")                               
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                pic = imdb.get('poster')
                poster = pic.replace('.jpg', "._V1_UX360.jpg")
                await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md")
            except Exception as e:
                logger.exception(e)
                await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="md") 
        else: 
            await message.reply_text(
                text=f"๐๐ผ แแญแฏแแบแธ  [{message.from_user.first_name}]({message.from_user.username}) แแฑ.... ๐๐\n\n[{message.from_user.first_name}]({message.from_user.username}) แแพแฌแแฌ ๐๐ป {message.text}๐๐ป  แแญแฏ แแแบแแแบแแฎแแพแแพแญแแฌ แแผแแฑแธแแฌแธแแแบแแฑแฌแบแโฅ๏ธ๐...\n\n๐๐ผ Request by : [{message.from_user.first_name}]({message.from_user.username})\n\nโ๏ธ Join Main Channel \nโ๏ธ K-Series  ๐๐ป @MKSVIPLINK \nโ๏ธ Movie      ๐๐ป @KPMOVIELIST\nโ๏ธ ๐๐ฅ๐ก๐ค๐๐๐๐ ๐ฝ๐ฎ   : ๐๐ค ๐๐๐๐ฃ๐ ๐๐๐ฎ ๐ฅฐ",         
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode="md"
            )

                                                             
@Client.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    clicked = query.from_user.id
    typed = query.message.reply_to_message.from_user.id

    if (clicked == typed) or (clicked in AUTH_USERS):

        if query.data.startswith("next"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("แแแบแแแบ แแปแฝแแบแฏแแบแ แแแบแแฑแทแแปแบแแฑแฌแแบแธแแปแฌแธแแฒแแพ แแแบแแฏแกแแฝแแบ แแแบแธแแญแฏ แกแแฏแถแธแแผแฏแแฑแแแบแ แแปแฑแธแแฐแธแแผแฏแ แแฑแฌแแบแธแแญแฏแแปแแบแแญแฏ แแแบแแถแแฑแธแแญแฏแทแแซแ",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("โ แแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซ โ", url="https://t.me/Movie_Zone_KP/3")]
                )
                buttons.append(
                    [InlineKeyboardButton("โช ๐๐๐๐ ๐ฃ๐๐๐", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"๐ฐ ๐ฃ๐๐๐ {int(index)+2}/{data['total']} ๐ฐ", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐๐ป ๐๐๐ ๐๐๐ซ๐ข๐๐ฌ ๐๐๐ฆ๐๐๐ซ แแแบแแแบ ๐", url="https://t.me/Kpautoreply_bot")]
                )
               

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("โ แแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซ โ", url="https://t.me/Movie_Zone_KP/3")]
                )
                buttons.append(
                    [InlineKeyboardButton("โช ๐๐๐๐", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton(f"๐ฃ๐๐๐ {int(index)+2}/{data['total']}", callback_data="pages"),InlineKeyboardButton("๐๐๐ฑ๐ญ โฉ", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐๐ป ๐๐๐ ๐๐๐ซ๐ข๐๐ฌ ๐๐๐ฆ๐๐๐ซ แแแบแแแบ ๐", url="https://t.me/Kpautoreply_bot")]
                )
                

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("แแแบแแแบ แแปแฝแแบแฏแแบแ แแแบแแฑแทแแปแบแแฑแฌแแบแธแแปแฌแธแแฒแแพ แแแบแแฏแกแแฝแแบ แแแบแธแแญแฏ แกแแฏแถแธแแผแฏแแฑแแแบแ แแปแฑแธแแฐแธแแผแฏแ แแฑแฌแแบแธแแญแฏแแปแแบแแญแฏ แแแบแแถแแฑแธแแญแฏแทแแซแ.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("โ แแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซ โ", url="https://t.me/Movie_Zone_KP/3")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐๐๐ฑ๐ญ ๐๐๐?๐ โฉ", callback_data=f"next_{int(index)-1}_{keyword}"),InlineKeyboardButton(f"๐ฐ ๐ฃ๐๐๐ {int(index)}/{data['total']} ๐ฐ", callback_data="pages")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐๐ป ๐๐๐ ๐๐๐ซ๐ข๐๐ฌ ๐๐๐ฆ๐๐๐ซ แแแบแแแบ ๐", url="https://t.me/Kpautoreply_bot")]
                )
                
  
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("โ แแแบแแแแแบแแฎแแญแฏแแพแญแแบแแผแฎแธ Link Join แแซ โ", url="https://t.me/Movie_Zone_KP/3")]
                )
                buttons.append(
                    [InlineKeyboardButton("โช ๐๐๐๐", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton(f"๐ฃ๐๐๐ {int(index)}/{data['total']}", callback_data="pages"),InlineKeyboardButton("๐๐๐ฑ๐ญ โฉ", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton("๐๐ป ๐๐๐ ๐๐๐ซ๐ข๐๐ฌ ๐๐๐ฆ๐๐๐ซ แแแบแแแบ ๐", url="https://t.me/Kpautoreply_bot")]
                )
               
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data == "pages":
            await query.answer()


        elif query.data == "start_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("HELP", callback_data="help_data"),
                    InlineKeyboardButton("ABOUT", callback_data="about_data")],
                [InlineKeyboardButton("โฃ๏ธ JOIN MAIN CHANNEL โฃ๏ธ ", url="https://t.me/MKSVIPLINK")],
                [InlineKeyboardButton("โญ๏ธ JOIN OUR CHANNEL โญ๏ธ", url="https://t.me/Movie_Zone_KP/3")],
                [InlineKeyboardButton('๐? English Series ๐?', url='https://t.me/Serieslists'), 
                    InlineKeyboardButton('๐? Thai Series๐?', url='https://t.me/ThaiSeries_MTS')],
                [InlineKeyboardButton('๐? Chinese Series๐?', url='https://t.me/Chinese_Series_MCS'), 
                    InlineKeyboardButton('๐? Anime Series๐?', url='https://t.me/Anime_Animation_Series')],
                [InlineKeyboardButton('๐? Bollywood Series๐?', url='https://t.me/+1-VidI6DzaA0MDA1'),
                    InlineKeyboardButton('๐? Korean Series๐?', url='https://t.me/MKSVIPLINK')],
                [InlineKeyboardButton('๐? Request Group ๐?', url='https://t.me/MKS_REQUESTGroup'),
                    InlineKeyboardButton('๐? VIP All Series  ๐?', url='https://t.me/Kpautoreply_bot')]
            ])

            await query.message.edit_text(
                script.START_MSG.format(query.from_user.mention),
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "help_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="start_data"),
                    InlineKeyboardButton("ABOUT ", callback_data="about_data")],
                [InlineKeyboardButton("โฃ๏ธ SUPPORT โฃ๏ธ", url="https://t.me/MKS_RequestGroup")],
                [InlineKeyboardButton("โญ๏ธ JOIN OUR CHANNEL โญ๏ธ", url="https://t.me/Movie_Zone_KP/3")],
                [InlineKeyboardButton('๐? English Series ๐?', url='https://t.me/Serieslists'), 
                    InlineKeyboardButton('๐? Thai Series๐?', url='https://t.me/ThaiSeries_MTS')],
                [InlineKeyboardButton('๐? Chinese Series๐?', url='https://t.me/Chinese_Series_MCS'), 
                    InlineKeyboardButton('๐? Anime Series๐?', url='https://t.me/Anime_Animation_Series')],
                [InlineKeyboardButton('๐? Bollywood Series๐?', url='https://t.me/+1-VidI6DzaA0MDA1'),
                    InlineKeyboardButton('๐? Korean Series๐?', url='https://t.me/MKSVIPLINK')],
                [InlineKeyboardButton('๐? Request Group ๐?', url='https://t.me/MKS_REQUESTGroup'),
                    InlineKeyboardButton('๐? VIP All Series  ๐?', url='https://t.me/Kpautoreply_bot')]
            ])

            await query.message.edit_text(
                script.HELP_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "about_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="help_data"),
                    InlineKeyboardButton("START", callback_data="start_data")],
                [InlineKeyboardButton(" โฃ๏ธ SOURCE CODE โฃ๏ธ", url="https://t.me/kopainglay15")],
                [InlineKeyboardButton("โญ๏ธ JOIN OUR CHANNEL โญ๏ธ", url="https://t.me/Movie_Zone_KP/3")],
                [InlineKeyboardButton('๐? English Series ๐?', url='https://t.me/Serieslists'), 
                    InlineKeyboardButton('๐? Thai Series๐?', url='https://t.me/ThaiSeries_MTS')],
                [InlineKeyboardButton('๐? Chinese Series๐?', url='https://t.me/Chinese_Series_MCS'), 
                    InlineKeyboardButton('๐? Anime Series๐?', url='https://t.me/Anime_Animation_Series')],
                [InlineKeyboardButton('๐? Bollywood Series๐?', url='https://t.me/+1-VidI6DzaA0MDA1'),
                    InlineKeyboardButton('๐? Korean Series๐?', url='https://t.me/MKSVIPLINK')],
                [InlineKeyboardButton('๐? Request Group ๐?', url='https://t.me/MKS_REQUESTGroup'),
                    InlineKeyboardButton('๐? VIP All Series  ๐?', url='https://t.me/Kpautoreply_bot')]
            ])

            await query.message.edit_text(
                script.ABOUT_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "delallconfirm":
            await query.message.delete()
            await deleteallfilters(client, query.message)
        
        elif query.data == "delallcancel":
            await query.message.reply_to_message.delete()
            await query.message.delete()

    else:
        await query.answer("๐ แแแบแธแแแบแธ แแฐแแปแฌแธแแญแฏแแบแแฌแธแแฌแแฑ \n\n๐  แแพแญแแบแแปแแบแแแบ แแแฏแแฒ แแฝแแญแฏแแญแฏแแบแแซ ๐!!\n\nUploaded By :Ko Paing โฃ๏ธ!",show_alert=True)


def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]  







#f"<b>๐๐ผ แแญแฏแแบแธ  {message.from_user.mention} แแฑ.... ๐๐\n\n{message.from_user.mention} แแพแฌแแฌ ๐๐ป {message.text}๐๐ป  แแญแฏ แแแบแแแบแแฎแแพแแพแญแแฌ แแผแแฑแธแแฌแธแแแบแแฑแฌแบแโฅ๏ธ๐...\n\n<b>๐๐ผ Request by : {message.from_user.mention}</b>\n\n<b>โ๏ธ Join Main Channel \nโ๏ธ K-Series  ๐๐ป @MKSVIPLINK \nโ๏ธ Movie      ๐๐ป @KPMOVIELIST</b>\n</b>โ๏ธ ๐๐ฅ๐ก๐ค๐๐๐๐ ๐ฝ๐ฎ   : ๐๐ค ๐๐๐๐ฃ๐ ๐๐๐ฎ ๐ฅฐ</a>",       
