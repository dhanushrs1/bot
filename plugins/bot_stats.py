import time
import psutil
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified, MessageTooLong
from info import ADMINS, LOG_CHANNEL, USERNAME
from database.users_chats_db import db
from database.ia_filterdb import get_files_db_size, Media
from utils import get_size, get_readable_time, temp
from Script import script
from datetime import datetime

# --- CONFIGURATION for your MongoDB Plan ---
# Set your plan's storage limit in GB. For the free tier, this is 0.5 GB.
# For other plans (e.g., M2), check your MongoDB dashboard. Example: 5 GB.
MAIN_DB_STORAGE_LIMIT_GB = 0.5
FILE_DB_STORAGE_LIMIT_GB = 0.5
GROUPS_PER_PAGE = 10

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    if temp.ME in [u.id for u in message.new_chat_members]:
        # Check if group is already in the database
        if not await db.get_chat(message.chat.id):
            total = await bot.get_chat_members_count(message.chat.id)
            user = message.from_user.mention if message.from_user else "an Admin"
            try:
                group_link = await message.chat.export_invite_link()
            except Exception:
                group_link = "N/A"
            
            # Add to database
            await db.add_chat(message.chat.id, message.chat.title)
            
            # Send log message
            await bot.send_message(
                LOG_CHANNEL,
                script.NEW_GROUP_TXT.format(
                    temp.B_LINK, message.chat.title, message.chat.id,
                    message.chat.username or "N/A", group_link, total, user
                ),
                parse_mode=ParseMode.HTML
            )
            
            # Send welcome message
            btn = [[InlineKeyboardButton("⚡️ Support Group ⚡️", url=f"https://t.me/{USERNAME}")]]
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"<b>Thank you for adding me to {message.chat.title}!</b>\n\n"
                     "To get started, please make me an admin in this group.\n"
                     "If you have any questions, feel free to ask in our support group.",
                reply_markup=InlineKeyboardMarkup(btn),
                parse_mode=ParseMode.HTML
            )


# --- Command for Bot to Leave a Group ---
@Client.on_message(filters.command("leave") & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply("<b>Usage:</b> <code>/leave -100xxxxxxxx</code>")
        
    chat_id_str = message.command[1]
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No reason provided."

    try:
        chat_id = int(chat_id_str)
        await bot.send_message(
            chat_id=chat_id,
            text=f"😔 I'm leaving this group as per my owner's request.\n\n"
                 f"<b>Reason:</b> <code>{reason}</code>\n\n"
                 f"If you wish to add me back, please contact my owner: @{USERNAME}",
            parse_mode=ParseMode.HTML
        )
        await bot.leave_chat(chat_id)
        await db.delete_chat(chat_id)
        await message.reply(f"✅ Successfully left the group: <code>{chat_id}</code>")
    except Exception as e:
        await message.reply(f"<b>Error leaving group <code>{chat_id_str}</code>:</b>\n<code>{e}</code>")


# --- Invite Link Generator ---
@Client.on_message(filters.command("invite") & filters.private & filters.user(ADMINS))
async def invite(client, message):
    if len(message.command) < 2:
        return await message.reply("<b>Usage:</b> <code>/invite -100xxxxxxxx</code>")
    
    to_gen_inv_link = message.command[1]
    
    try:
        link = await client.export_chat_invite_link(int(to_gen_inv_link))
        await message.reply(f"<b>Invite link for <code>{to_gen_inv_link}</code>:</b>\n{link}")
    except Exception as e:
        await message.reply(f"<b>Error generating invite link for <code>{to_gen_inv_link}</code>:</b>\n<code>{e}</code>")


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
        Media.count_documents() # This will now work
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


# --- Interactive Paginated List of Groups ---
@Client.on_message(filters.command("groups") & filters.user(ADMINS))
async def list_groups(bot, message):
    msg = await message.reply("<b>🔄 Processing... Please wait.</b>", parse_mode=ParseMode.HTML)
    await display_groups_page(bot, msg, 1)

async def display_groups_page(bot, message, page_number):
    chats_cursor = await db.get_all_chats()
    # Correctly convert async cursor to a list
    chats_list = [chat async for chat in chats_cursor]
    
    if not chats_list:
        return await message.edit_text("No groups found in the database.")

    total_pages = (len(chats_list) + GROUPS_PER_PAGE - 1) // GROUPS_PER_PAGE
    start_index = (page_number - 1) * GROUPS_PER_PAGE
    end_index = start_index + GROUPS_PER_PAGE
    
    out = f"<b>Total Groups in Database: {len(chats_list)}</b>\n\n"
    
    for i, chat in enumerate(chats_list[start_index:end_index], start=start_index + 1):
        try:
            chat_info = await bot.get_chat(chat['id'])
            members = await bot.get_chat_members_count(chat['id'])  # <-- Fix here
            out += f"<b>{i}. {chat['title']}</b>\n   - <b>ID:</b> <code>{chat['id']}</code>\n   - <b>Members:</b> <code>{members}</code>\n\n"
        except Exception as e:
            print(f"Error fetching chat {chat['id']}: {e}")
            out += f"<b>{i}. {chat['title']}</b>\n   - <b>ID:</b> <code>{chat['id']}</code>\n   - <i>Could not fetch details.</i>\n\n"

    buttons = []
    if total_pages > 1:
        nav_row = []
        if page_number > 1:
            nav_row.append(InlineKeyboardButton("⬅️ Back", callback_data=f"grp_nav_{page_number-1}"))
        
        nav_row.append(InlineKeyboardButton(f"Page {page_number}/{total_pages}", callback_data="noop")) # Added a noop callback for the page number button

        if page_number < total_pages:
            nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"grp_nav_{page_number+1}"))
        
        buttons.append(nav_row)
    
    try:
        await message.edit_text(out, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.HTML)
    except MessageTooLong:
        with open("groups_list.txt", "w+", encoding="utf-8") as f:
            f.write(out.replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", ""))
        await message.reply_document("groups_list.txt", caption="<b>List of all groups.</b>")
    except MessageNotModified:
        pass # Ignore if the page content is the same

@Client.on_callback_query(filters.regex(r"^grp_nav_"))
async def handle_group_nav(bot, query):
    page = int(query.data.split("_")[2])
    await display_groups_page(bot, query.message, page)

@Client.on_callback_query(filters.regex(r"^noop$"))
async def noop_callback(bot, query):
    """Handles callbacks for buttons that should do nothing, like page numbers."""
    await query.answer()