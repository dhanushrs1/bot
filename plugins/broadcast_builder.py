# plugins/broadcast_builder.py

import asyncio
import datetime
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, Message, ForceReply
)
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, PeerIdInvalid
from info import ADMINS
from database.users_chats_db import db
from utils import get_readable_time

# In-memory storage for the broadcast building process
broadcast_builders = {}

# --- Step 1: Start the Broadcast Builder ---
@Client.on_message(filters.command(["broadcast", "bcast"]) & filters.user(ADMINS))
async def start_broadcast_builder(client, message):
    admin_id = message.from_user.id
    broadcast_builders[admin_id] = {"state": "awaiting_content", "message": None, "buttons": []}
    await message.reply_text(
        "<b>🚀 Broadcast Builder Initiated</b>\n\n"
        "Please send me the content you want to broadcast. This can be text, a photo, or a video with a caption.",
        reply_markup=ForceReply(placeholder="Send your broadcast message here..."),
        parse_mode=ParseMode.HTML
    )

# --- Filter for admin replies during the build process ---
async def builder_input_filter(_, __, message: Message):
    if not (message.from_user and message.from_user.id in broadcast_builders):
        return False
    if message.text and message.text.startswith('/'):
        return False
    return True

# --- Step 2 & 3: Handle Admin's Content and Button Replies ---
@Client.on_message(filters.private & filters.create(builder_input_filter))
async def handle_builder_input(client, message):
    admin_id = message.from_user.id
    state_data = broadcast_builders[admin_id]
    current_state = state_data["state"]

    if current_state == "awaiting_content":
        state_data["message"] = message
        state_data["state"] = "awaiting_button_choice"
        await message.reply_text(
            "<b>✅ Content saved.</b>\n\nWould you like to add inline buttons to your message?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Yes, add buttons", callback_data="builder_add_buttons")],
                [InlineKeyboardButton("➡️ No, show preview", callback_data="builder_preview")]
            ])
        )

    elif current_state == "awaiting_buttons":
        text = message.text
        if " - " in text:
            try:
                button_text, button_data = text.split(" - ", 1)
                button_data = button_data.strip()
                if button_data.startswith("http"):
                    button = InlineKeyboardButton(button_text.strip(), url=button_data)
                else:
                    button = InlineKeyboardButton(button_text.strip(), callback_data=button_data)
                state_data["buttons"].append(button)
                await message.reply_text(f"Button '<b>{button_text}</b>' added. Add another or click 'Done'.", parse_mode=ParseMode.HTML)
            except Exception as e:
                await message.reply_text(f"<b>Error:</b> {e}\nPlease use format: <code>Button Text - URL</code>")
        else:
            await message.reply_text("<b>Invalid Format.</b> Please use: <code>Button Text - https://your.url</code>", parse_mode=ParseMode.HTML)

# --- Step 4 & 5: Handle Callbacks for Preview and Confirmation ---
@Client.on_callback_query(filters.regex(r"^builder_"))
async def handle_builder_callbacks(client, query):
    admin_id = query.from_user.id
    if admin_id not in broadcast_builders:
        return await query.answer("This session has expired. Please start over with /broadcast.", show_alert=True)

    action = query.data.split("_", 1)[1]
    state_data = broadcast_builders[admin_id]

    if action == "add_buttons":
        state_data["state"] = "awaiting_buttons"
        await query.message.edit_text(
            "<b>Button Creator</b>\n\n"
            "Send your buttons one by one in the format:\n"
            "<code>Button Text - https://your.url/here</code>\n\n"
            "When you're finished, click the 'Done' button below.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Done Adding Buttons", callback_data="builder_preview")]
            ]),
            parse_mode=ParseMode.HTML
        )

    elif action == "preview":
        if not state_data.get("message"):
            return await query.answer("Content not found. Please start over.", show_alert=True)

        state_data["state"] = "awaiting_confirmation"
        buttons_list = state_data["buttons"]
        button_rows = [buttons_list[i:i + 2] for i in range(0, len(buttons_list), 2)]
        reply_markup = InlineKeyboardMarkup(button_rows) if button_rows else None
        
        await query.message.delete()
        
        await state_data["message"].copy(
            chat_id=admin_id,
            reply_markup=reply_markup
        )
        
        await client.send_message(
            admin_id,
            "<b>Broadcast Preview</b>\n\nThis is the final preview. Ready to send it to all users?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Send Now", callback_data="builder_send")],
                [InlineKeyboardButton("❌ Cancel", callback_data="builder_cancel")]
            ]),
            parse_mode=ParseMode.HTML
        )

    elif action == "send":
        await query.message.edit_text("<b>⏳ Initializing broadcast...</b>\nThis may take a while. Please do not restart the bot.", parse_mode=ParseMode.HTML)
        
        broadcast_message = state_data["message"]
        buttons_list = state_data["buttons"]
        button_rows = [buttons_list[i:i + 2] for i in range(0, len(buttons_list), 2)]
        reply_markup = InlineKeyboardMarkup(button_rows) if button_rows else None
        
        total_users = await db.total_users_count()
        users_cursor = await db.get_all_users()
        
        success, blocked, deleted, failed = 0, 0, 0, 0
        start_time = datetime.datetime.now()
        
        # --- CORRECTED BROADCAST LOOP ---
        i = 0
        async for user_doc in users_cursor:
            i += 1
            user_id = user_doc['id']
            try:
                await broadcast_message.copy(user_id, reply_markup=reply_markup)
                success += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await broadcast_message.copy(user_id, reply_markup=reply_markup)
                success += 1
            except UserIsBlocked:
                blocked += 1
            except InputUserDeactivated:
                deleted += 1
            except (PeerIdInvalid, Exception):
                failed += 1

            if i % 50 == 0 or i == total_users:
                try:
                    await query.message.edit_text(
                        f"<b>📢 Broadcast in progress...</b>\n\n"
                        f"<b>Sent:</b> <code>{i} / {total_users}</code>\n"
                        f"<b>✅ Success:</b> <code>{success}</code>\n"
                        f"<b>🚫 Blocked:</b> <code>{blocked}</code>\n"
                        f"<b>🗑️ Deleted:</b> <code>{deleted}</code>\n"
                        f"<b>❌ Failed:</b> <code>{failed}</code>",
                        parse_mode=ParseMode.HTML
                    )
                except:
                    pass
        
        end_time = datetime.datetime.now()
        duration = get_readable_time((end_time - start_time).seconds)
        
        await query.message.edit_text(
            f"✅ <b>Broadcast Complete!</b>\n\n"
            f"<b>🗓️ Date:</b> <code>{start_time.strftime('%Y-%m-%d')}</code>\n"
            f"<b>⏳ Duration:</b> <code>{duration}</code>\n\n"
            f"📊 <b><u>Report:</u></b>\n"
            f"  - <b>Total Users:</b> <code>{total_users}</code>\n"
            f"  - <b>Successfully Sent:</b> <code>{success}</code>\n"
            f"  - <b>Blocked/Deleted:</b> <code>{blocked + deleted}</code>\n"
            f"  - <b>Failed:</b> <code>{failed}</code>",
            parse_mode=ParseMode.HTML
        )
        if admin_id in broadcast_builders:
            del broadcast_builders[admin_id]

    elif action == "cancel":
        await query.message.edit_text("<b>❌ Broadcast cancelled successfully.</b>", parse_mode=ParseMode.HTML)
        if admin_id in broadcast_builders:
            del broadcast_builders[admin_id]

    await query.answer()