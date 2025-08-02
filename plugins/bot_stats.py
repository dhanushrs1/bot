from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from info import ADMINS, LOG_CHANNEL, USERNAME
from database.users_chats_db import db
from database.ia_filterdb import Media, get_files_db_size
from utils import get_size, temp, get_readable_time
from pyrogram.enums import ParseMode
import asyncio
from Script import script
import psutil
import time

MAIN_DB_STORAGE_LIMIT_GB = 0.5  # Main database storage limit in GB
FILE_DB_STORAGE_LIMIT_GB = 0.5   # File index database storage limit in GB


@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    check = [u.id for u in message.new_chat_members]
    if temp.ME in check:
        if not await db.get_chat(message.chat.id):
            total = await bot.get_chat_members_count(message.chat.id)
            user = message.from_user.mention if message.from_user else "Dear"
            group_link = await message.chat.export_invite_link()
            await bot.send_message(
                LOG_CHANNEL,
                script.NEW_GROUP_TXT.format(
                    temp.B_LINK,
                    message.chat.title,
                    message.chat.id,
                    message.chat.username,
                    group_link,
                    total,
                    user,
                ),
                disable_web_page_preview=True,
            )
            await db.add_chat(message.chat.id, message.chat.title)
            btn = [[InlineKeyboardButton("⚡️ sᴜᴘᴘᴏʀᴛ ⚡️", url=USERNAME)]]
            reply_markup = InlineKeyboardMarkup(btn)
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"<b>☤ ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ {message.chat.title}\n\n🤖 ᴅᴏɴ’ᴛ ꜰᴏʀɢᴇᴛ ᴛᴏ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ 🤖\n\n㊝ ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ᴅᴏᴜʙᴛ ʏᴏᴜ ᴄʟᴇᴀʀ ɪᴛ ᴜsɪɴɢ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ㊜</b>",
                reply_markup=reply_markup,
            )


@Client.on_message(filters.command("leave") & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    r = message.text.split(None)
    if len(message.command) == 1:
        return await message.reply(
            "<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʟɪᴋᴇ ᴛʜɪꜱ `/leave -100******`</b>"
        )
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "ɴᴏ ʀᴇᴀꜱᴏɴ ᴘʀᴏᴠɪᴅᴇᴅ..."
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        btn = [[InlineKeyboardButton("⚡️ ᴏᴡɴᴇʀ ⚡️", url=USERNAME)]]
        reply_markup = InlineKeyboardMarkup(btn)
        await bot.send_message(
            chat_id=chat,
            text=f"😞 ʜᴇʟʟᴏ ᴅᴇᴀʀ,\nᴍʏ ᴏᴡɴᴇʀ ʜᴀꜱ ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ʟᴇᴀᴠᴇ ꜰʀᴏᴍ ɢʀᴏᴜᴘ ꜱᴏ ɪ ɢᴏ 😔\n\n🚫 ʀᴇᴀꜱᴏɴ ɪꜱ - <code>{reason}</code>\n\nɪꜰ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴀᴅᴅ ᴍᴇ ᴀɢᴀɪɴ ᴛʜᴇɴ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴏᴡɴᴇʀ 👇",
            reply_markup=reply_markup,
        )
        await bot.leave_chat(chat)
        await db.delete_chat(chat)
        await message.reply(f"<b>ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʟᴇꜰᴛ ꜰʀᴏᴍ ɢʀᴏᴜᴘ - `{chat}`</b>")
    except Exception as e:
        await message.reply(f"<b>🚫 ᴇʀʀᴏʀ - `{e}`</b>")


@Client.on_message(filters.command("groups") & filters.user(ADMINS))
async def groups_list(bot, message):
    msg = await message.reply("<b>Searching...</b>")
    chats = await db.get_all_chats()
    out = "Groups saved in the database:\n\n"
    count = 1
    async for chat in chats:
        chat_info = await bot.get_chat(chat["id"])
        members_count = (
            chat_info.members_count if chat_info.members_count else "Unknown"
        )
        out += f"<b>{count}. Title - `{chat['title']}`\nID - `{chat['id']}`\nMembers - `{members_count}`</b>"
        out += "\n\n"
        count += 1
    try:
        if count > 1:
            await msg.edit_text(out)
        else:
            await msg.edit_text("<b>No groups found</b>")
    except MessageTooLong:
        with open("chats.txt", "w+") as outfile:
            outfile.write(out)
        await message.reply_document("chats.txt", caption="<b>List of all groups</b>")


@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def get_stats_dashboard(client, message):
    """
    Handles the /stats command and displays an advanced, dual-database dashboard for admins.
    """
    processing_msg = await message.reply_text("<b>🔄 Generating stats dashboard...</b>", parse_mode=ParseMode.HTML)

    # --- Fetch all stats in parallel for speed ---
    db1_size, db2_size, total_users, total_groups, new_users_today, new_groups_today, total_files = await asyncio.gather(
        db.get_db_size(),
        get_files_db_size(),
        db.total_users_count(),
        db.total_chat_count(),
        db.get_new_users_today(),
        db.get_new_groups_today(),
        Media.count_documents() 
    )
    
    # --- Main Database (Users & Groups) Calculation ---
    db1_limit_bytes = MAIN_DB_STORAGE_LIMIT_GB * 1024 * 1024 * 1024
    db1_used_str = get_size(db1_size)
    db1_limit_str = get_size(db1_limit_bytes)
    db1_remaining_bytes = db1_limit_bytes - db1_size
    db1_remaining_str = get_size(db1_remaining_bytes if db1_remaining_bytes > 0 else 0)
    
    # --- File Index Database Calculation ---
    db2_limit_bytes = FILE_DB_STORAGE_LIMIT_GB * 1024 * 1024 * 1024
    db2_used_str = get_size(db2_size)
    db2_limit_str = get_size(db2_limit_bytes)
    db2_remaining_bytes = db2_limit_bytes - db2_size
    db2_remaining_str = get_size(db2_remaining_bytes if db2_remaining_bytes > 0 else 0)
    db2_usage_percent_str = round((db2_size / db2_limit_bytes) * 100, 2) if db2_limit_bytes > 0 else 0

    # --- System & Bot Status ---
    try:
        uptime = get_readable_time(time.time() - client.start_time)
    except AttributeError:
        uptime = "N/A"
        
    ram_usage = f"{psutil.virtual_memory().percent}%"
    cpu_usage = f"{psutil.cpu_percent()}%"

    # --- Format the Final Dashboard Text with Separated Sections ---
    stats_text = f"""
📊 <b><u>Bot Statistics Dashboard</u></b>

<b><u>👤 User Analytics:</u></b>
  - <b>Total Users:</b> <code>{total_users}</code>
  - <b>New Users Today:</b> <code>{new_users_today}</code>

<b><u>🗃️Main Database (Users & Groups):</u></b>
  - <b>Total Groups:</b> <code>{total_groups}</code>
  - <b>New Groups Today:</b> <code>{new_groups_today}</code>
  - <b>Size Used:</b> <code>{db1_used_str}</code> / <code>{db1_limit_str}</code>
  - <b>Storage Remaining:</b> <code>{db1_remaining_str}</code>

<b><u>📁 File Index Database:</u></b>
  - <b>Total Files Indexed:</b> <code>{total_files}</code>
  - <b>Size Used:</b> <code>{db2_used_str}</code> / <code>{db2_limit_str}</code>
  - <b>Storage Remaining:</b> <code>{db2_remaining_str}</code>
  - <b>Usage Percentage:</b> <code>{db2_usage_percent_str}%</code>

<b><u>⚙️ System & Bot Status:</u></b>
  - <b>Bot Uptime:</b> <code>{uptime}</code>
  - <b>CPU Usage:</b> <code>{cpu_usage}</code>
  - <b>RAM Usage:</b> <code>{ram_usage}</code>
"""
    await processing_msg.edit_text(stats_text, parse_mode=ParseMode.HTML)

<<<<<<< HEAD

@Client.on_message(filters.command("invite") & filters.private & filters.user(ADMINS))
async def invite(client, message):
    toGenInvLink = message.command[1]
    if len(toGenInvLink) != 14:
        return await message.reply(
            "Invalid chat id\nAdd -100 before chat id if You did not add any yet."
        )
    try:
        link = await client.export_chat_invite_link(toGenInvLink)
        await message.reply(link)
    except Exception as e:
        print(f"Error while generating invite link : {e}\nFor chat:{toGenInvLink}")
        await message.reply(
            f"Error while generating invite link : {e}\nFor chat:{toGenInvLink}"
        )
=======
>>>>>>> bbc8edc642eb7c13d7afb2883b774a61d89dfbdc
