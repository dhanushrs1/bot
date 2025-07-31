# --| This code created by: Jisshu_bots & SilentXBotz |--#
import re
import hashlib
import asyncio
from info import *
from utils import *
from pyrogram import Client, filters
from database.users_chats_db import db
from database.ia_filterdb import save_file, unpack_new_file_id
import aiohttp
from typing import Optional
from collections import defaultdict

CAPTION_LANGUAGES = [
    "Bhojpuri",
    "Hindi",
    "Bengali",
    "Tamil",
    "English",
    "Bangla",
    "Telugu",
    "Malayalam",
    "Kannada",
    "Marathi",
    "Punjabi",
    "Bengoli",
    "Gujrati",
    "Korean",
    "Gujarati",
    "Spanish",
    "French",
    "German",
    "Chinese",
    "Arabic",
    "Portuguese",
    "Russian",
    "Japanese",
    "Odia",
    "Assamese",
    "Urdu",
]

UPDATE_CAPTION = """<b>𝖭𝖤𝖶 {} 𝖠𝖣𝖣𝖤𝖣 ✅</b>

🎬 <b>{} {}</b>
🔰 <b>Quality:</b> {}
🎧 <b>Audio:</b> {}

<b>Telegram Files</b>

{}

Powered by @hd_cinema_updates</b>"""

QUALITY_CAPTION = """📦 {} : {}\n"""

notified_movies = set()
movie_files = defaultdict(list)
POST_DELAY = 10
processing_movies = set()

media_filter = filters.document | filters.video | filters.audio


@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    bot_id = bot.me.id
    media = getattr(message, message.media.value, None)
    if media.mime_type in ["video/mp4", "video/x-matroska", "document/mp4"]:
        media.file_type = message.media.value
        media.caption = message.caption
        success_sts = await save_file(media)
        if success_sts == "suc" and await db.get_send_movie_update_status(bot_id):
            file_id, file_ref = unpack_new_file_id(media.file_id)
            await queue_movie_file(bot, media)


async def queue_movie_file(bot, media):
    try:
        file_name = await movie_name_format(media.file_name)
        caption = await movie_name_format(media.caption)
        year_match = re.search(r"\b(19|20)\d{2}\b", caption)
        year = year_match.group(0) if year_match else None
        season_match = re.search(r"(?i)(?:s|season)0*(\d{1,2})", caption) or re.search(
            r"(?i)(?:s|season)0*(\d{1,2})", file_name
        )
        if year:
            file_name = file_name[: file_name.find(year) + 4]
        elif season_match:
            season = season_match.group(1)
            file_name = file_name[: file_name.find(season) + 1]
        quality = await get_qualities(caption) or "HDRip"
        jisshuquality = await Jisshu_qualities(caption, media.file_name) or "720p"
        language = (
            ", ".join(
                [lang for lang in CAPTION_LANGUAGES if lang.lower() in caption.lower()]
            )
            or "Not Idea"
        )
        file_size_str = format_file_size(media.file_size)
        file_id, file_ref = unpack_new_file_id(media.file_id)
        movie_files[file_name].append(
            {
                "quality": quality,
                "jisshuquality": jisshuquality,
                "file_id": file_id,
                "file_size": file_size_str,
                "caption": caption,
                "language": language,
                "year": year,
            }
        )
        if file_name in processing_movies:
            return
        processing_movies.add(file_name)
        try:
            await asyncio.sleep(POST_DELAY)
            if file_name in movie_files:
                await send_movie_update(bot, file_name, movie_files[file_name])
                del movie_files[file_name]
        finally:
            processing_movies.remove(file_name)
    except Exception as e:
        print(f"Error in queue_movie_file: {e}")
        if file_name in processing_movies:
            processing_movies.remove(file_name)
        await bot.send_message(LOG_CHANNEL, f"Failed to send movie update. Error - {e}'\n\n<blockquote>If you don’t understand this error, you can ask in our support group: @hdcinemasupport .</blockquote>")

async def send_movie_update(bot, file_name, files):
    try:
        if file_name in notified_movies:
            return
        notified_movies.add(file_name)

        imdb_data = await get_imdb(file_name)
        title = imdb_data.get("title", file_name)
        year_match = re.search(r"\b(19|20)\d{2}\b", file_name)
        year = year_match.group(0) if year_match else None
        poster = await fetch_movie_poster(title, files[0]["year"])
        kind = imdb_data.get("kind", "").strip().upper().replace(" ", "_") if imdb_data else ""
        if kind == "TV_SERIES":
           kind = "SERIES"
        languages = set()
        for file in files:
            if file["language"] != "Not Idea":
                languages.update(file["language"].split(", "))
        language = ", ".join(sorted(languages)) or "Not Idea"

        episode_pattern = re.compile(r"S(\d{1,2})E(\d{1,2})", re.IGNORECASE)
        combined_pattern = re.compile(r"S(\d{1,2})\s*E(\d{1,2})[-~]E?(\d{1,2})", re.IGNORECASE)
        episode_map = defaultdict(dict)
        combined_links = []

        for file in files:
            caption = file["caption"]
            quality = file.get("jisshuquality") or file.get("quality") or "Unknown"
            size = file["file_size"]
            file_id = file['file_id']
            match = episode_pattern.search(caption)
            combined_match = combined_pattern.search(caption)

            if match:
                ep = f"S{int(match.group(1)):02d}E{int(match.group(2)):02d}"
                episode_map[ep][quality] = file
            elif combined_match:
                season = f"S{int(combined_match.group(1)):02d}"
                ep_range = f"E{int(combined_match.group(2)):02d}-{int(combined_match.group(3)):02d}"
                ep = f"{season}{ep_range}"
                combined_links.append(f"📦 {ep} ({quality}) : <a href='https://t.me/{temp.U_NAME}?start=file_0_{file_id}'>{size}</a>")
            elif re.search(r"complete|completed|batch|combined", caption, re.IGNORECASE):
                combined_links.append(f"📦 ({quality}) : <a href='https://t.me/{temp.U_NAME}?start=file_0_{file_id}'>{size}</a>")

        quality_text = ""

        for ep, qualities in sorted(episode_map.items()):
            parts = []
            for quality in sorted(qualities.keys()):
                f = qualities[quality]
                link = f"<a href='https://t.me/{temp.U_NAME}?start=file_0_{f['file_id']}'>{quality}</a>"
                parts.append(link)
            joined = " - ".join(parts)
            quality_text += f"📦 {ep} : {joined}\n"

        if combined_links:
            quality_text += "\n<b>COMBiNED</b> ✅\n\n"
            quality_text += "\n".join(combined_links) + "\n"
            
        if not quality_text:
            quality_groups = defaultdict(list)
            for file in files:
                quality = file.get("jisshuquality") or file.get("quality") or "Unknown"
                quality_groups[quality].append(file)

            for quality, q_files in sorted(quality_groups.items()):
                links = [f"<a href='https://t.me/{temp.U_NAME}?start=file_0_{f['file_id']}'>{f['file_size']}</a>" for f in q_files]
                line = f"📦 {quality} : " + " | ".join(links)
                quality_text += line + "\n"

        image_url = poster or "https://i.ibb.co/N21Ww127/Poster-Not-Found.png"
        full_caption = UPDATE_CAPTION.format(kind, title, year, files[0]['quality'], language, quality_text)

        movie_update_channel = await db.movies_update_channel_id()
        await bot.send_photo(
            chat_id=movie_update_channel if movie_update_channel else MOVIE_UPDATE_CHANNEL,
            photo=image_url,
            caption=full_caption,
            parse_mode=enums.ParseMode.HTML
        )

    except Exception as e:
        print('Failed to send movie update. Error - ', e)
        await bot.send_message(LOG_CHANNEL, f"Failed to send movie update. Error - {e}'\n\n<blockquote>If you don’t understand this error, you can ask in our support group: @hdcinemasupport.</blockquote>")


async def get_imdb(file_name):
    try:
        formatted_name = await movie_name_format(file_name)
        imdb = await get_poster(formatted_name)
        if not imdb:
            return {}
        return {
            "title": imdb.get("title", formatted_name),
            "kind": imdb.get("kind", "Movie"),
            "year": imdb.get("year"),
            "url": imdb.get("url"),
        }
    except Exception as e:
        print(f"IMDB fetch error: {e}")
        return {}


async def fetch_movie_poster(title: str, year: Optional[int] = None) -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        query = title.strip().replace(" ", "+")
        url = f"https://jisshuapis.vercel.app/api.php?query={query}"
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as res:
                if res.status != 200:
                    print(f"API Error: HTTP {res.status}")
                    return None
                data = await res.json()

                for key in ["jisshu-2", "jisshu-3", "jisshu-4"]:
                    posters = data.get(key)
                    if posters and isinstance(posters, list) and posters:
                        return posters[0]

                print(f"No Poster Found in jisshu-2/3/4 for Title: {title}")
                return None

        except aiohttp.ClientError as e:
            print(f"Network Error: {e}")
            return None
        except asyncio.TimeoutError:
            print("Request Timed Out")
            return None
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return None


def generate_unique_id(movie_name):
    return hashlib.md5(movie_name.encode("utf-8")).hexdigest()[:5]


async def get_qualities(text):
    qualities = [
        "480p",
        "720p",
        "720p HEVC",
        "1080p",
        "ORG",
        "org",
        "hdcam",
        "HDCAM",
        "HQ",
        "hq",
        "HDRip",
        "hdrip",
        "camrip",
        "WEB-DL",
        "CAMRip",
        "hdtc",
        "predvd",
        "DVDscr",
        "dvdscr",
        "dvdrip",
        "HDTC",
        "dvdscreen",
        "HDTS",
        "hdts",
    ]
    found_qualities = [q for q in qualities if q.lower() in text.lower()]
    return ", ".join(found_qualities) or "HDRip"


async def Jisshu_qualities(text, file_name):
    qualities = ["480p", "720p", "720p HEVC", "1080p", "1080p HEVC", "2160p"]
    combined_text = (text.lower() + " " + file_name.lower()).strip()
    if "hevc" in combined_text:
        for quality in qualities:
            if "HEVC" in quality and quality.split()[0].lower() in combined_text:
                return quality
    for quality in qualities:
        if "HEVC" not in quality and quality.lower() in combined_text:
            return quality
    return "720p"


async def movie_name_format(file_name):
    filename = re.sub(
        r"http\S+",
        "",
        re.sub(r"@\w+|#\w+", "", file_name)
        .replace("_", " ")
        .replace("[", "")
        .replace("]", "")
        .replace("(", "")
        .replace(")", "")
        .replace("{", "")
        .replace("}", "")
        .replace(".", " ")
        .replace("@", "")
        .replace(":", "")
        .replace(";", "")
        .replace("'", "")
        .replace("-", "")
        .replace("!", ""),
    ).strip()
    return filename


def format_file_size(size_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"
