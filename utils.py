import logging
from pyrogram.errors import (
    InputUserDeactivated,
    UserNotParticipant,
    FloodWait,
    UserIsBlocked,
    PeerIdInvalid,
)
from info import AUTH_CHANNEL, LONG_IMDB_DESCRIPTION, START_IMG
from imdb import Cinemagoer
import asyncio
from pyrogram.types import Message
from pyrogram import enums
import pytz
import re
import os
from shortzy import Shortzy
from datetime import datetime
from typing import Any
from database.users_chats_db import db


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BANNED = {}
imdb = Cinemagoer()


class temp(object):
    ME = None
    CURRENT = int(os.environ.get("SKIP", 2))
    CANCEL = False
    U_NAME = None
    B_NAME = None
    B_LINK = None
    SETTINGS = {}
    FILES_ID = {}
    USERS_CANCEL = False
    GROUPS_CANCEL = False
    CHAT = {}
    BANNED_USERS = []
    BANNED_CHATS = []


def formate_file_name(file_name):
    file_name = " ".join(
        filter(
            lambda x: not x.startswith("[")
            and not x.startswith("@")
            and not x.startswith("www."),
            file_name.split(),
        )
    )
    return file_name


async def is_req_subscribed(bot, query):
    if await db.find_join_req(query.from_user.id):
        return True
    try:
        user = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
    except UserNotParticipant:
        pass
    except Exception as e:
        print(e)
    else:
        if user.status != enums.ChatMemberStatus.BANNED:
            return True
    return False


async def is_subscribed(bot, user_id, channel_id):
    try:
        user = await bot.get_chat_member(channel_id, user_id)
    except UserNotParticipant:
        pass
    except Exception:
        pass
    else:
        if user.status != enums.ChatMemberStatus.BANNED:
            return True
    return False


async def get_poster(query, bulk=False, id=False, file=None):
    if not id:
        query = (query.strip()).lower()
        title = query
        year = re.findall(r"[1-2]\d{3}$", query, re.IGNORECASE)
        if year:
            year = list_to_str(year[:1])
            title = (query.replace(year, "")).strip()
        elif file is not None:
            year = re.findall(r"[1-2]\d{3}", file, re.IGNORECASE)
            if year:
                year = list_to_str(year[:1])
        else:
            year = None
        movieid = imdb.search_movie(title.lower(), results=10)
        if not movieid:
            return None
        if year:
            filtered = list(filter(lambda k: str(k.get("year")) == str(year), movieid))
            if not filtered:
                filtered = movieid
        else:
            filtered = movieid
        movieid = list(
            filter(lambda k: k.get("kind") in ["movie", "tv series"], filtered)
        )
        if not movieid:
            movieid = filtered
        if bulk:
            return movieid
        movieid = movieid[0].movieID
    else:
        movieid = query
    movie = imdb.get_movie(movieid)
    if movie.get("original air date"):
        date = movie["original air date"]
    elif movie.get("year"):
        date = movie.get("year")
    else:
        date = "N/A"
    plot = ""
    if not LONG_IMDB_DESCRIPTION:
        plot = movie.get("plot")
        if plot and len(plot) > 0:
            plot = plot[0]
    else:
        plot = movie.get("plot outline")
    if plot and len(plot) > 800:
        plot = plot[0:800] + "..."

    return {
        "title": movie.get("title"),
        "votes": movie.get("votes"),
        "aka": list_to_str(movie.get("akas")),
        "seasons": movie.get("number of seasons"),
        "box_office": movie.get("box office"),
        "localized_title": movie.get("localized title"),
        "kind": movie.get("kind"),
        "imdb_id": f"tt{movie.get('imdbID')}",
        "cast": list_to_str(movie.get("cast")),
        "runtime": list_to_str(movie.get("runtimes")),
        "countries": list_to_str(movie.get("countries")),
        "certificates": list_to_str(movie.get("certificates")),
        "languages": list_to_str(movie.get("languages")),
        "director": list_to_str(movie.get("director")),
        "writer": list_to_str(movie.get("writer")),
        "producer": list_to_str(movie.get("producer")),
        "composer": list_to_str(movie.get("composer")),
        "cinematographer": list_to_str(movie.get("cinematographer")),
        "music_team": list_to_str(movie.get("music department")),
        "distributors": list_to_str(movie.get("distributors")),
        "release_date": date,
        "year": movie.get("year"),
        "genres": list_to_str(movie.get("genres")),
        "poster": movie.get("full-size cover url", START_IMG),
        "plot": plot,
        "rating": str(movie.get("rating")),
        "url": f"https://www.imdb.com/title/tt{movieid}",
    }


async def users_broadcast(user_id, message, is_pin):
    try:
        m = await message.copy(chat_id=user_id)
        if is_pin:
            await m.pin(both_sides=True)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await users_broadcast(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - Removed from Database, since Blocked the bot.")
        await db.delete_user(user_id)
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception:
        return False, "Error"


async def groups_broadcast(chat_id, message, is_pin):
    try:
        m = await message.copy(chat_id=chat_id)
        if is_pin:
            try:
                await m.pin()
            except:
                pass
        return "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await groups_broadcast(chat_id, message)
    except Exception:
        await db.delete_chat(chat_id)
        logging.info(f"{chat_id}-Removed from Database.")
        return "Error"


async def get_settings(group_id):
    settings = await db.get_settings(int(group_id))
    return settings


async def save_group_settings(group_id, key, value):
    current = await get_settings(group_id)
    current[key] = value
    await db.update_settings(group_id, current)


def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])


def get_name(name):
    regex = re.sub(r"@\w+", "", name)
    return regex


def list_to_str(k):
    if not k:
        return "N/A"
    elif len(k) == 1:
        return str(k[0])
    else:
        return ", ".join(str(item) for item in k)


async def get_shortlink(
    link, grp_id, is_second_shortener=False, is_third_shortener=False
):
    settings = await get_settings(grp_id)
    if is_third_shortener:
        api, site = settings["api_three"], settings["shortner_three"]
    else:
        if is_second_shortener:
            api, site = settings["api_two"], settings["shortner_two"]
        else:
            api, site = settings["api"], settings["shortner"]
    shortzy = Shortzy(api, site)
    try:
        link = await shortzy.convert(link)
    except Exception:
        link = await shortzy.get_quick_link(link)
    return link


def get_file_id(message: "Message") -> Any:
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    )
    if message.media:
        for attr in media_types:
            media = getattr(message, attr, None)
            if media:
                setattr(media, "message_type", attr)
                return media


# def get_hash(media_msg: Message) -> str:
#    media = get_file_id(media_msg)
#   return getattr(media, "file_unique_id", "")[:6]


def get_status():
    tz = pytz.timezone("Asia/Colombo")
    hour = datetime.now(tz).hour

    if 4 <= hour < 11:
        return "𝑮𝒐𝒐𝒅 𝒎𝒐𝒓𝒏𝒊𝒏𝒈! 🌄"
    elif 11 <= hour < 16:
        return "𝑮𝒐𝒐𝒅 𝒂𝒇𝒕𝒆𝒓𝒏𝒐𝒐𝒏! 🌞"
    elif 16 <= hour < 20:
        return "𝑮𝒐𝒐𝒅 𝒆𝒗𝒆𝒏𝒊𝒏𝒈! 🌆"
    elif 20 <= hour < 24:
        return "𝑮𝒐𝒐𝒅 𝒏𝒊𝒈𝒉𝒕! 🌙"
    else:  # 0–3 AM
        return "𝑳𝒂𝒕𝒆 𝒏𝒊𝒈𝒉𝒕 𝒗𝒊𝒃𝒆𝒔! 🌌"


async def is_check_admin(bot, chat_id, user_id):
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in [
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER,
        ]
    except:
        return False


async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        unit = ""
        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1
        unit = ts[index:].lstrip()
        if value:
            value = int(value)
        return value, unit

    value, unit = extract_value_and_unit(time_string)
    if unit == "s":
        return value
    elif unit == "min":
        return value * 60
    elif unit == "hour":
        return value * 3600
    elif unit == "day":
        return value * 86400
    elif unit == "month":
        return value * 86400 * 30
    elif unit == "year":
        return value * 86400 * 365
    else:
        return 0


def get_readable_time(seconds: int) -> str:
    """Returns a human-readable time format like 1d 2h 3m 4s"""
    if not seconds:
        return "0s"
        
    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d "
        
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h "
        
    (minutes, sec) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m "
        
    seconds = int(sec)
    if seconds != 0:
        result += f"{seconds}s"
        
    return result.strip()


async def save_default_settings(id):
    await db.reset_group_settings(id)
    current = await db.get_settings(id)
    temp.SETTINGS.update({id: current})
