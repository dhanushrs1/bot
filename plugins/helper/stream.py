from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from info import URL, LOG_CHANNEL, ADMINS
from urllib.parse import quote_plus
from Jisshu.util.file_properties import get_name, get_hash, get_media_file_size
from Jisshu.util.human_readable import humanbytes
import humanize
from database.users_chats_db import db
import asyncio

@Client.on_message(filters.group & filters.command("streams"))
async def stream_start(client, message):
    # This check now correctly uses the group's ID from message.chat.id
    stream_mode_enabled = await db.get_stream_mode(message.chat.id)
    
    # Check if the user is an admin
    is_admin = message.from_user.id in ADMINS

    # If the feature is disabled and the user is not an admin, stop them.
    if not stream_mode_enabled and not is_admin:
        await message.reply_text("This feature has been disabled by the admin for regular users.")
        return

    # Ask the user to send the file in a private message to the bot
    ask_msg = await message.reply_text("Please forward the file you want to stream to me in a private message.")

    try:
        # Wait for the user to forward a message to the bot in PM
        msg = await client.listen(
            chat_id=message.from_user.id,
            timeout=300  # 5-minute timeout
        )
    except asyncio.TimeoutError:
        await ask_msg.edit_text("You took too long to send the file. Please try the command again in the group.")
        return

    if not msg.media:
        return await client.send_message(message.from_user.id, "**The message you sent is not a supported media file.**")

    if msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        file = getattr(msg, msg.media.value)
        filename = file.file_name
        filesize = humanize.naturalsize(file.file_size)
        fileid = file.file_id
        user_id = message.from_user.id
        username = message.from_user.mention

        log_msg = await client.send_cached_media(
            chat_id=LOG_CHANNEL,
            file_id=fileid,
        )
        
        fileName = quote_plus(get_name(log_msg))
        stream = f"{URL}watch/{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}/{fileName}?hash={get_hash(log_msg)}"

        await log_msg.reply_text(
            text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🚀 Fast Download 🚀", url=download),
                        InlineKeyboardButton("🖥️ Watch online 🖥️", url=stream),
                    ]
                ]
            ),
        )
        
        rm = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("sᴛʀᴇᴀᴍ 🖥", url=stream),
                    InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=download),
                ]
            ]
        )
        msg_text = """<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n\n<b> 🖥ᴡᴀᴛᴄʜ  :</b> <i>{}</i>\n\n<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ</b>"""

        await client.send_message(
            chat_id=message.from_user.id,
            text=msg_text.format(
                get_name(log_msg),
                humanbytes(get_media_file_size(msg)),
                download,
                stream,
            ),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=rm,
        )
        
# --- Admin Commands to Toggle Stream Mode ---

@Client.on_message(filters.command("streammode_on") & filters.user(ADMINS))
async def streammode_on(client, message):
    current_mode = await db.get_stream_mode(message.chat.id)
    if current_mode:
        await message.reply_text("Stream mode is already **enabled** for this group.")
        return
    await db.update_stream_mode(message.chat.id, True)
    await message.reply_text("✅ Stream mode has been **enabled** for all users in this group.")

@Client.on_message(filters.command("streammode_off") & filters.user(ADMINS))
async def streammode_off(client, message):
    current_mode = await db.get_stream_mode(message.chat.id)
    if not current_mode:
        await message.reply_text("Stream mode is already **disabled** for this group.")
        return
    await db.update_stream_mode(message.chat.id, False)
    await message.reply_text("❌ Stream mode has been **disabled**. Only admins can use the command in this group now.")