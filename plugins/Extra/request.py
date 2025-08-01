# plugins/Extra/request.py

import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import REQUEST_CHANNEL, ADMINS
from database.ia_filterdb import get_search_results

@Client.on_message(filters.command("request") & filters.private)
async def private_request_command(client, message):
    if len(message.command) == 1:
        await message.reply_text(
            "<b>Usage:</b> /request <movie_name>\n\n"
            "<b>Example:</b> /request The Dark Knight"
        )
        return

    # --- Give immediate feedback to the user ---
    processing_message = await message.reply_text("⏳ Processing your request...")

    query = message.text.split(" ", 1)[1]
    
    # 1. Check if the movie already exists in the database
    try:
        files, _, total_results = await get_search_results(query)
        if total_results > 0:
            await processing_message.edit_text(
                f"✅ Good news! We already have files for **{query}**.\n\n"
                "Please search for it directly in the bot or in our main group."
            )
            return
    except Exception as e:
        print(f"Error checking database for request: {e}")
        await processing_message.edit_text("An error occurred while checking our records. Please try again later.")
        return

    # 2. Format the request with a timestamp
    user_info = message.from_user.mention
    user_id = message.from_user.id
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # IST Time can be added if needed

    request_text = (f"<b>✨ New Movie Request!</b>\n\n"
                    f"<b>🎬 Movie Name:</b> {query}\n"
                    f"<b>🗣️ Requested by:</b> {user_info}\n"
                    f"<b>🆔 User ID:</b> <code>{user_id}</code>\n"
                    f"<b>🗓️ Time:</b> {timestamp}")

    # 3. Add admin action buttons
    admin_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Mark as Filled", callback_data=f"req_filled#{user_id}#{query}")],
        [InlineKeyboardButton("❌ Reject Request", callback_data=f"req_reject#{user_id}#{query}")]
    ])
    
    # 4. Send the request and handle potential errors
    try:
        await client.send_message(
            REQUEST_CHANNEL,
            text=request_text,
            reply_markup=admin_buttons
        )
        # 5. Confirm to the user that the request was submitted
        await processing_message.edit_text(
            "✅ Your request has been successfully submitted to our admins!\n\n"
            "We will notify you once it has been fulfilled."
        )
    except Exception as e:
        print(f"Failed to send request to channel: {e}")
        await processing_message.edit_text(
            "❌ Sorry, something went wrong while submitting your request. "
            "Please try again later or contact support."
        )

# --- Add the callback handlers below this line ---

@Client.on_callback_query(filters.regex(r"^req_"))
async def handle_request_callback(client, query):
    if query.from_user.id not in ADMINS:
        return await query.answer("This is for admins only!", show_alert=True)

    action, user_id_str, movie_name = query.data.split("#")
    user_id = int(user_id_str)

    if action == "req_filled":
        # Notify the user that their request is complete
        await client.send_message(
            user_id,
            f"🎉 Great news! Your request for **{movie_name}** has been fulfilled.\n\n"
            "You can now search for it in the bot."
        )
        await query.message.edit_text(
            f"{query.message.text.split('---')[0]}\n\n---\n<b>Status:</b> ✅ Filled by {query.from_user.mention}"
        )

    elif action == "req_reject":
        # Notify the user that their request was rejected
        await client.send_message(
            user_id,
            f"😔 We're sorry, but your request for **{movie_name}** has been rejected.\n\n"
            "This may be because the file is not available or the request was invalid."
        )
        await query.message.edit_text(
            f"{query.message.text.split('---')[0]}\n\n---\n<b>Status:</b> ❌ Rejected by {query.from_user.mention}"
        )
    
    await query.answer("Action completed.")