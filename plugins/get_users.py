import os
import math
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified
from info import ADMINS
from database.users_chats_db import db

# --- Constants ---
USERS_PER_PAGE = 10

# --- Helper Function to Create Pages ---
async def build_users_page(client, page_number):
    """Builds a page of users with navigation buttons."""
    start_index = (page_number - 1) * USERS_PER_PAGE
    
    try:
        users_slice = await db.get_users_slice(start_index, USERS_PER_PAGE)
        total_users = await db.total_users_count()
    except Exception as e:
        error_text = f"**Database Error:**\n\n`{e}`\n\nPlease ensure you have added the `get_users_slice` and `total_users_count` functions to your `users_chats_db.py` file."
        return error_text, None

    if not users_slice and page_number == 1:
        return "**There are no users in the database yet.**", None

    text = f"**👤 All Bot Users - Page {page_number}**\n\n"
    count = start_index + 1
    for user_data in users_slice:
        user_id = user_data['id']
        name = user_data.get('name', 'N/A')
        is_premium = await db.has_premium_access(user_id)
        premium_icon = "⭐" if is_premium else "▪️"
        
        text += f"{premium_icon} `{count}.` **{name}**\n       **ID:** `{user_id}`\n"
        count += 1
        
    total_pages = math.ceil(total_users / USERS_PER_PAGE)
    
    buttons = []
    nav_row = []
    if page_number > 1:
        nav_row.append(InlineKeyboardButton("⬅️ Back", callback_data=f"nav_users_{page_number-1}"))
    
    nav_row.append(InlineKeyboardButton(f"📄 {page_number}/{total_pages}", callback_data="noop"))
    
    if page_number < total_pages:
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data=f"nav_users_{page_number+1}"))
    
    if nav_row:
        buttons.append(nav_row)

    buttons.append([
        InlineKeyboardButton("📥 Download Full List", callback_data="download_users"),
        InlineKeyboardButton("❌ Close", callback_data="close_users"),
    ])
    
    return text, InlineKeyboardMarkup(buttons)

# --- Command Handler ---
@Client.on_message(filters.command("allusers") & filters.user(ADMINS))
async def all_users_command(client, message):
    """Initializes the user list viewer and keeps the original command."""
    # Reply to the user's command message.
    status_msg = await message.reply_text(
        text="`Processing...`",
        quote=True 
    )
    
    text, reply_markup = await build_users_page(client, 1)
    
    if reply_markup:
        await status_msg.edit(text, reply_markup=reply_markup)
    else:
        await status_msg.edit(text)
    
    # The line "await message.delete()" has been removed.

# --- Callback Query Handler ---
@Client.on_callback_query(filters.regex(r"^(nav_users_|download_users|close_users|noop)"))
async def users_callback_handler(client, query):
    if query.data == "noop":
        await query.answer()
        return

    if query.data == "close_users":
        # Now this will delete the bot's message, leaving the user's command.
        await query.message.delete()
        return

    try:
        if query.data.startswith("nav_users_"):
            page = int(query.data.split("_")[2])
            text, reply_markup = await build_users_page(client, page)
            await query.message.edit(text, reply_markup=reply_markup)

        elif query.data == "download_users":
            await query.answer("Preparing the full user list...", show_alert=True)
            
            all_users_cursor = await db.get_all_users()
            total_users = await db.total_users_count()
            
            file_path = "all_bot_users.txt"
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"--- Total Users: {total_users} ---\n\n")
                count = 1
                async for user in all_users_cursor:
                    user_id = user['id']
                    name = user.get('name', 'N/A')
                    is_premium = "Yes" if await db.has_premium_access(user_id) else "No"
                    file.write(f"{count}. ID: {user_id} | Name: {name} | Premium: {is_premium}\n")
                    count += 1
            
            await client.send_document(
                chat_id=query.from_user.id,
                document=file_path,
                caption=f"Here is the full list of **{total_users}** users."
            )
            os.remove(file_path)
            # We don't delete the message anymore, so the admin can keep Browse.

    except MessageNotModified:
        await query.answer("You are already on this page.", show_alert=True)
    except Exception as e:
        await query.answer(f"An error occurred: {e}", show_alert=True)