import math
import secrets
import string

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

# Make sure these are defined in your info.py file
from info import LOG_CHANNEL, UPI_ID, OWNER_USERNAME, PRICING_POINTS


# This dictionary tracks the state of each user. It's crucial for the reply handling.
user_states = {}


# --- ADVANCED PRICING & SAVINGS LOGIC ---
def calculate_price(days):
    """Calculates a fair price using interpolation between pricing points."""
    if not isinstance(days, int) or days <= 0: return None
    sorted_tiers = sorted(PRICING_POINTS.keys())
    if days in sorted_tiers: return PRICING_POINTS[days]
    lower_tier, upper_tier = 1, sorted_tiers[-1]
    for d in sorted_tiers:
        if days > d: lower_tier = d
        if days < d:
            upper_tier = d
            break
    lower_price, upper_price = PRICING_POINTS[lower_tier], PRICING_POINTS[upper_tier]
    progress = (days - lower_tier) / (upper_tier - lower_tier)
    calculated_price = math.ceil(lower_price + (upper_price - lower_price) * progress)
    return min(calculated_price, PRICING_POINTS[upper_tier])

def get_savings_info(days, price):
    """Generates a compelling savings tip."""
    sorted_tiers = sorted(PRICING_POINTS.keys())
    for tier in sorted_tiers:
        if tier > days:
            extra_cost = PRICING_POINTS[tier] - price
            if 0 < extra_cost <= (price * 0.5):
                return {'days': tier, 'price': PRICING_POINTS[tier], 'extra_cost': extra_cost}
    return None


# --- BOT HANDLERS (REFINED FOR ROBUSTNESS & UI) ---

@Client.on_callback_query(filters.regex("custom_plan"))
async def prompt_for_days(client, callback_query):
    """Starts the flow by asking for the number of days."""
    user_id = callback_query.from_user.id
    
    # Send a new message that prompts the user to reply.
    sent_message = await client.send_message(
        chat_id=user_id,
        text="<b>➡️ Of course! Please send me your desired plan duration in days.</b>\n\n(e.g., 10, 45, 100)",
        reply_markup=ForceReply(placeholder="Enter days...")
    )
    
    # Store the message ID to identify the user's reply.
    user_states[user_id] = {"prompt_message_id": sent_message.id}
    await callback_query.answer()


@Client.on_message(filters.private & filters.reply)
async def handle_custom_plan_reply(client, message):
    """Handles the user's reply, calculates the price, and presents a confirmation."""
    user_id = message.from_user.id
    state = user_states.get(user_id)

    # --- ROBUST STATE HANDLING ---
    # This check ensures the bot only processes replies to its specific prompt.
    if not state or not message.reply_to_message or message.reply_to_message.id != state.get("prompt_message_id"):
        return

    try:
        days = int(message.text.strip())
        if not (1 <= days <= 365):
            await message.reply_text("<b>Invalid Duration</b>\nPlease enter a number between 1 and 365 days (1 years).", parse_mode=enums.ParseMode.HTML)
            return
    except (ValueError, TypeError):
        await message.reply_text("<b>Invalid Input</b>\nPlease enter a valid number.", parse_mode=enums.ParseMode.HTML)
        return

    # Clean up the state and the original prompt message.
    del user_states[user_id]
    try:
        await client.delete_messages(user_id, message.reply_to_message.id)
    except:
        pass # Fails silently if message is already gone

    price = calculate_price(days)
    price_per_day = round(price / days, 2)
    hdc_id = 'HDC-' + ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    savings_tip = get_savings_info(days, price)

    # --- IMPRESSIVE UI ---
    response_text = f"""
<b>📊 Here is your personalized quote:</b>

🗓️ <b>Duration:</b> <code>{days} days</code>
💳 <b>Total Price:</b> <code>₹{price}</code>
📈 _This works out to just ~₹{price_per_day} per day!_
"""

    if savings_tip:
        deal = savings_tip
        response_text += f"\n\n💡 <b>Smart Saver Tip:</b> For just <b>₹{deal['extra_cost']} more</b>, you can upgrade to our <b>{deal['days']}-day plan</b> and lock in a better daily rate!"

    confirmation_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ ʏᴇꜱ, ʟᴏᴏᴋꜱ ɢᴏᴏᴅ - ᴄᴏɴᴛɪɴᴜᴇ", callback_data=f"accept_{days}_{price}_{hdc_id}")],
        [
            InlineKeyboardButton("🔄 ᴄʜᴀɴɢᴇ ᴅᴜʀᴀᴛɪᴏɴ", callback_data="custom_plan"),
            InlineKeyboardButton("✖️ ᴄᴀɴᴄᴇʟ", callback_data="close_prompt")
        ]
    ])
    
    await message.reply_text(response_text, parse_mode=enums.ParseMode.HTML, reply_markup=confirmation_buttons)


@Client.on_callback_query(filters.regex(r"accept_"))
async def accept_and_pay(client, callback_query):
    """Logs the request and presents the final payment instructions."""
    try:
        _, days, price, hdc_id = callback_query.data.split("_")
        days, price = int(days), int(price)
    except:
        await callback_query.answer("Error: Invalid request. Please try again.", show_alert=True)
        return
    
    user = callback_query.from_user
    log_message = f"""
#PAYMENT_INITIATED

👤 <b>User:</b> {user.mention} ({user.id})
🏷️ <b>Username:</b> @{user.username or 'N/A'}
📅 <b>Plan:</b> {days} days for ₹{price}
🔑 <b>HDC ID:</b> <code>{hdc_id}</code> (tap to copy)
"""
    try:
        await client.send_message(chat_id=LOG_CHANNEL, text=log_message, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        print(f"Error sending log to LOG_CHANNEL: {e}")

    payment_buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("📸 ꜱᴇɴᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ᴛᴏ ᴀᴅᴍɪɴ", url=f"https://t.me/{OWNER_USERNAME}")]]
    )
    
    payment_text = f"""
✅ <b><u>Final Step: Complete Your Payment</u></b>

Please follow these steps carefully:

1. Pay exactly <b><u>₹{price}</u></b> to the UPI ID below.
2. <b>Crucial:</b> You must add <code>{hdc_id}</code> to your payment's note/message field.

─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
   <b>Amount:</b> <code>₹{price}</code>
   <b>UPI ID:</b> <code>{UPI_ID}</code>
   <b>Note:</b> <code>{hdc_id}</code> (tap to copy)
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

After paying, use the button below to send the screenshot for verification.
"""
    await callback_query.message.edit_text(text=payment_text, parse_mode=enums.ParseMode.HTML, reply_markup=payment_buttons)
    await callback_query.answer()


@Client.on_callback_query(filters.regex("close_prompt"))
async def close_prompt(client, callback_query):
    """Cleans up the chat when a user cancels the process."""
    await callback_query.message.edit_text("<i>Custom plan creation cancelled. Feel free to start over anytime!</i>", parse_mode=enums.ParseMode.HTML)
    await callback_query.answer()