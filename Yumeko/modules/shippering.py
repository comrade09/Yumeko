# Copyright (C) 2021 dihan official

# This file is part of Mizuhara (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from Yumeko import pbot as app
from pyrogram import filters
import random
from datetime import datetime
from pymongo import MongoClient

MONGO_DB_URI = "mongodb+srv://SOME1HING:AyN5a6YZMVXFdi9E@shikimori-bot.nomdo.mongodb.net/Shikimori-Bot?retryWrites=true&w=majority"

client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["Rikka_couples"]

from typing import Dict, List, Union


# Couple Chooser

coupledb = db.couple


async def _get_lovers(chat_id: int):
    lovers = coupledb.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["couple"]
    else:
        lovers = {}
    return lovers


async def get_couple(chat_id: int, date: str):
    lovers = await _get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    else:
        return False


async def save_couple(chat_id: int, date: str, couple: dict):
    lovers = await _get_lovers(chat_id)
    lovers[date] = couple
    coupledb.update_one({"chat_id": chat_id}, {"$set": {"couple": lovers}}, upsert=True)


# Date and time
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(' ')
    return dt_list


def dt_tom():
    a = str(int(dt()[0].split('/')[0]) + 1)+"/" + \
        dt()[0].split('/')[1]+"/" + dt()[0].split('/')[2]
    return a


today = str(dt()[0])
tomorrow = str(dt_tom())


@app.on_message(filters.command("couples"))
async def couple(_, message):
    if message.chat.type == "private":
        await message.reply_text("This command only works in groups.")
        return
    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            list_of_users = []
            async for i in app.get_chat_members(message.chat.id):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)
            if len(list_of_users) < 2:
                await message.reply_text("Not enough users")
                return
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            c1_mention = (await app.get_users(c1_id)).mention
            c2_mention = (await app.get_users(c2_id)).mention

            couple_selection_message = f"""**Couple of the day:**
{c1_mention} + {c2_mention} = ❤️
Congratulations from Tyrant Eye's Wielder 🎊
__New couple of the day may be chosen at 12AM {tomorrow}__"""
            await app.send_message(
                message.chat.id,
                text=couple_selection_message
            )
            couple = {
                "c1_id": c1_id,
                "c2_id": c2_id
            }
            await save_couple(chat_id, today, couple)

        elif is_selected:
            c1_id = int(is_selected['c1_id'])
            c2_id = int(is_selected['c2_id'])
            c1_name = (await app.get_users(c1_id)).first_name
            c2_name = (await app.get_users(c2_id)).first_name
            couple_selection_message = f"""Couple of the day:
[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = ❤️
__New couple of the day may be chosen at 12AM {tomorrow}__"""
            await app.send_message(
                message.chat.id,
                text=couple_selection_message
            )
    except Exception as e:
        print(e)
        await message.reply_text(e)



__help__ = """
- /couples - To Choose Couple Of The Day ❤
 """
__mod_name__ = "Couples"