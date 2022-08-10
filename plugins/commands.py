#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from script import script


@Client.on_message(filters.command(["start"]) & filters.private)
async def start(client, message):
    try:
        await message.reply_text(
            text=script.START_MSG.format(message.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("HELP", callback_data="help_data"),
                        InlineKeyboardButton("ABOUT", callback_data="about_data"),
                    ],
                    [
                        InlineKeyboardButton(
                            "⭕️ JOIN OUR CHANNEL ⭕️", url="https://t.me/Movie_Zone_KP/3"),
                    ],
                    [
                        InlineKeyboardButton('💠 English Series 💠', url='https://t.me/Serieslists'), 
                        InlineKeyboardButton('💠 Thai Series💠', url='https://t.me/ThaiSeries_MTS')
                    ],
                    [
                        InlineKeyboardButton('💠 Chinese Series💠', url='https://t.me/Chinese_Series_MCS'), 
                        InlineKeyboardButton('💠 Anime Series💠', url='https://t.me/Anime_Animation_Series')
                    ],
                    [
                        InlineKeyboardButton('💠 Bollywood Series💠', url='https://t.me/+1-VidI6DzaA0MDA1'),
                        InlineKeyboardButton('💠 Korean Series💠', url='https://t.me/MKSVIPLINK')
                    ],
                    [
                        InlineKeyboardButton('💠 Request Group 💠', url='https://t.me/MKS_REQUESTGroup'),
                        InlineKeyboardButton('💠 VIP All Series  💠', url='https://t.me/Kpautoreply_bot')
                    ]
                ]
            ),
            reply_to_message_id=message.message_id
        )
    except:
        pass

@Client.on_message(filters.command(["help"]) & filters.private)
async def help(client, message):
    try:
        await message.reply_text(
            text=script.HELP_MSG,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("BACK", callback_data="start_data"),
                        InlineKeyboardButton("ABOUT", callback_data="about_data"),
                    ],
                    [
                        InlineKeyboardButton(
                            "⭕️ JOIN OUR CHANNEL ⭕️", url="https://t.me/Movie_Zone_KP/3"),
                    ],
                    [
                        InlineKeyboardButton('💠 English Series 💠', url='https://t.me/Serieslists'), 
                        InlineKeyboardButton('💠 Thai Series💠', url='https://t.me/ThaiSeries_MTS')
                    ],
                    [
                        InlineKeyboardButton('💠 Chinese Series💠', url='https://t.me/Chinese_Series_MCS'), 
                        InlineKeyboardButton('💠 Anime Series💠', url='https://t.me/Anime_Animation_Series')
                    ],
                    [
                        InlineKeyboardButton('💠 Bollywood Series💠', url='https://t.me/+1-VidI6DzaA0MDA1'),
                        InlineKeyboardButton('💠 Korean Series💠', url='https://t.me/MKSVIPLINK')
                    ],
                    [
                        InlineKeyboardButton('💠 Request Group 💠', url='https://t.me/MKS_REQUESTGroup'),
                        InlineKeyboardButton('💠 VIP All Series  💠', url='https://t.me/Kpautoreply_bot')
                    ]
                ]
            ),
            reply_to_message_id=message.message_id
        )
    except:
        pass

@Client.on_message(filters.command(["about"]) & filters.private)
async def about(client, message):
    try:
        await message.reply_text(
            text=script.ABOUT_MSG,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("BACK", callback_data="help_data"),
                        InlineKeyboardButton("START", callback_data="start_data"),
                    ],
                    [
                        InlineKeyboardButton(
                            "⭕️ JOIN OUR CHANNEL ⭕️", url="https://t.me/Movie_Zone_KP/3"),
                    ],
                    [
                        InlineKeyboardButton('💠 English Series 💠', url='https://t.me/Serieslists'), 
                        InlineKeyboardButton('💠 Thai Series💠', url='https://t.me/ThaiSeries_MTS')
                    ],
                    [
                        InlineKeyboardButton('💠 Chinese Series💠', url='https://t.me/Chinese_Series_MCS'), 
                        InlineKeyboardButton('💠 Anime Series💠', url='https://t.me/Anime_Animation_Series')
                    ],
                    [
                        InlineKeyboardButton('💠 Bollywood Series💠', url='https://t.me/+1-VidI6DzaA0MDA1'),
                        InlineKeyboardButton('💠 Korean Series💠', url='https://t.me/MKSVIPLINK')
                    ],
                    [
                        InlineKeyboardButton('💠 Request Group 💠', url='https://t.me/MKS_REQUESTGroup'),
                        InlineKeyboardButton('💠 VIP All Series  💠', url='https://t.me/Kpautoreply_bot')
                    ],
                    [
                        InlineKeyboardButton(
                            "SOURCE CODE", url="https://t.me/kopainglay15")
                    ]
                ]
            ),
            reply_to_message_id=message.message_id
        )
    except:
        pass
