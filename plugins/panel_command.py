from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from info import ADMINS

# --- MAIN COMMAND HANDLER ---
@Client.on_message(filters.command("panel") & filters.private)
async def panel_command(client, message):
    """
    Handles the /panel command.
    """
    if message.from_user.id in ADMINS:
        # --- Admin's Main Menu ---
        await message.reply_text(
            text="<b>🤖 Bot Control Panel</b>\n\nWelcome, Admin! Select a category to view the available commands.",
            reply_markup=get_main_admin_keyboard(),
            parse_mode=ParseMode.HTML
        )
    else:
        # --- Regular User's Menu ---
        user_text = "<b>👋 Welcome to the Bot!</b>\n\nHere is a list of commands available to you:\n"
        user_text += get_user_commands_text()
        await message.reply_text(
            text=user_text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

# --- CALLBACK HANDLER FOR ALL MENU BUTTONS ---
@Client.on_callback_query(filters.regex(r"^botpanel#"))
async def botpanel_callback(client, query):
    if query.from_user.id not in ADMINS:
        return await query.answer("This menu is for admins only.", show_alert=True)
    
    _, menu_type = query.data.split("#")
    
    text = ""
    keyboard = get_back_button()

    if menu_type == "admin":
        text = "<b>👑 Admin Control Panel</b>\n\nCommands for bot administration and management."
        text += await get_admin_commands_text(client)  # Pass the 'client' object
    elif menu_type == "group":
        text = "<b>👥 Group Management Panel</b>\n\nCommands for controlling the bot in groups."
        text += get_group_commands_text()
    elif menu_type == "user":
        text = "<b>👤 User Command List (Admin View)</b>\n\nThis is the command list that regular users see."
        text += get_user_commands_text()
    elif menu_type == "main":
        text = "<b>🤖 Bot Control Panel</b>\n\nWelcome back! Please select a panel."
        keyboard = get_main_admin_keyboard()

    await query.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )
    await query.answer()

# --- HELPER FUNCTIONS TO GENERATE TEXT ---

async def get_admin_commands_text(client):  # Accept 'client' as an argument
    """Generates the complete Admin Commands text with status indicators."""
    
    bot_id = client.me.id
    
    # Get the current status of the features
    pm_search_status = "✅ ON" if await db.get_pm_search_status(bot_id) else "❌ OFF"
    movie_update_status = "✅ ON" if await db.get_send_movie_update_status(bot_id) else "❌ OFF"
    stream_mode_status = "✅ ON" if await db.get_stream_mode_global() else "❌ OFF"

    return f"""
<hr>
<b><u>⚙️ Global Bot Settings</u></b>
<code>/pm_search_on</code> | <code>/pm_search_off</code> - PM Search: <b>{pm_search_status}</b>
<code>/movie_update_on</code> | <code>/movie_update_off</code> - Movie Update: <b>{movie_update_status}</b>
<code>/stream_on</code> | <code>/stream_off</code> - Stream Mode: <b>{stream_mode_status}</b>

<b><u>📊 Core & Statistics</u></b>
<code>/stats</code> - View bot usage statistics.
<code>/allusers</code> - List all users of the bot.
<code>/groups</code> - List all groups the bot is in.
<code>/channel</code> - List all indexed channels.
<code>/refresh</code> - Reset a user's free trial status.

<b><u>📢 Broadcast & Communication</u></b>
<code>/broadcast</code> - Send a message to all users.
<code>/grp_broadcast</code> - Send a message to all groups.
<code>/send</code> - Reply to a message to send it to a user ID.

<b><u>👤 User Management</u></b>
<code>/ban</code> & <code>/unban</code> - Ban or unban a user from the bot.
<code>/add_premium</code> - Grant premium access to a user.
<code>/remove_premium</code> - Revoke a user's premium access.
<code>/premium_users</code> - List all users with premium.

<b><u>🗂️ File & Index Management</u></b>
<code>/index</code> - Index files from a channel.
<code>/delete</code> - Reply to a file to delete it from the DB.
<code>/deleteall</code> - ⚠️ Clear all indexed files from the DB.
<code>/del_file</code> & <code>/deletefiles</code> - Delete files from DB by keyword.

<b><u>🔗 Content & Links</u></b>
<code>/set_muc</code> - Set the movie update channel.
<code>/setlist</code> & <code>/clearlist</code> - Manage the top trending list.

<b><u>💰 Ads & Monetization</u></b>
<code>/add_redeem</code> - Generate premium redeem codes.
<code>/set_ads</code> | <code>/ads</code> | <code>/del_ads</code> - Manage advertisements.

<b><u>🛠️ Advanced</u></b>
<code>/commands</code> - Sets the bot's command list on Telegram.
<code>/admin_cmds</code> - Displays the list of admin commands.
<code>/delreq</code> - Delete all pending join requests for a channel.
<code>/invite</code> - Generate an invite link for a channel.
"""

def get_group_commands_text():
    """Generates the complete Group Admin Commands text."""
    return """
<hr>
<b><u>⚙️ Main Group Settings</u></b>
<code>/settings</code> - View and change all settings for a group.
<code>/details</code> - Show all current settings for a group.
<code>/reset_group</code> - ⚠️ Reset all settings to default.
<code>/grp_cmds</code> - Displays the list of group commands.

<b><u>🌊 Per-Group Stream Mode</u></b>
<code>/streammode_on</code> | <code>/streammode_off</code> - Overrides the global setting for a specific group.

<b><u>🎨 Customization</u></b>
<code>/set_template</code> - Define a custom IMDB info template.
<code>/set_caption</code> - Define a custom file caption.

<b><u>🔐 User Verification</u></b>
<code>/verifyon</code> or <code>/verifyoff</code> - Toggle the user verification system.
<code>/set_verify</code>, <code>_2</code>, <code>_3</code> - Set verification shortener URLs.
<code>/set_tutorial</code>, <code>_2</code>, <code>_3</code> - Set verification tutorial links.
<code>/set_time_2</code>, <code>_3</code> - Set time gaps between verification steps.

<b><u>🔗 Other Controls</u></b>
<code>/set_fsub</code> & <code>/remove_fsub</code> - Manage Force Subscribe.
<code>/set_log</code> - Set a log channel for group activity.
"""

def get_user_commands_text():
    """Generates the complete User Commands text."""
    # The /help command is replaced by /panel in this new system
    return """
<b><u>👋 Basic Commands</u></b>
<code>/start</code> - Starts the bot.
<code>/panel</code> - Shows this help menu.
<code>/id</code> - Get your unique Telegram ID.

<b><u>💎 Premium & Plans</u></b>
<code>/plan</code> - View premium membership plans.
<code>/myplan</code> - Check your current subscription.
<code>/redeem</code> - Redeem a premium gift code.
<code>/refer</code> - Get your referral link to earn premium.

<b><u>🎬 Content & Fun</u></b>
<code>/most</code> & <code>/mostlist</code> - See the most searched queries.
<code>/trend</code> & <code>/trendlist</code> - Discover currently trending movies.
<code>/font</code> - Generate text in stylish fonts.
<code>/stickerid</code> - Get the ID of a sticker.

<b><u>🔗 Utilities</u></b>
<code>/telegraph</code>, <code>/img</code>, <code>/cup</code> - Upload media to a link.
<code>/stream</code> - Get a direct streaming link for a file.
"""

# --- HELPER FUNCTIONS FOR KEYBOARDS ---
def get_main_admin_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 Admin Panel", callback_data="botpanel#admin")],
        [InlineKeyboardButton("👥 Group Management", callback_data="botpanel#group")],
        [InlineKeyboardButton("👤 View User Commands", callback_data="botpanel#user")]
    ])

def get_back_button():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("⬅️ Back to Main Panel", callback_data="botpanel#main")
    ]])