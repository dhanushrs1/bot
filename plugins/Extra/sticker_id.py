from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("stickerid"))
async def sticker_id(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        await message.reply_text("Please reply to a sticker to get its ID.")
        return

    sticker = message.reply_to_message.sticker
    await message.reply_text(f"**Sticker ID:** `{sticker.file_id}`")