from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, ADMIN_ID, PRIVATE_CHANNEL_ID, MAIN_CHANNEL

bot = Client("FileStoreBot", bot_token=BOT_TOKEN, api_id=29167872, api_hash="f26b4e46f6d6e5ad36f480e73357425d")

# /start command
@bot.on_message(filters.command("start"))
async def start(_, message):
    if len(message.command) > 1:
        file_id = message.command[1]
        try:
            # Check if user joined the channel
            user = await bot.get_chat_member(MAIN_CHANNEL, message.from_user.id)
            if user.status in ["member", "administrator", "creator"]:
                await bot.copy_message(chat_id=message.chat.id, from_chat_id=PRIVATE_CHANNEL_ID, message_id=int(file_id))
            else:
                await message.reply_text(
                    f"🚫 First join our channel {MAIN_CHANNEL} to access files.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{MAIN_CHANNEL.strip('@')}")],
                        [InlineKeyboardButton("✅ I Joined", callback_data=f"check_{file_id}")]
                    ])
                )
        except Exception as e:
            await message.reply_text("❌ Invalid or expired link.")
    else:
        await message.reply_text(f"👋 Hello {message.from_user.mention},\n\nSend me any file and I’ll generate a sharable link (Admin only).")

# Check joined or not
@bot.on_callback_query(filters.regex(r"check_(.*)"))
async def check_join(_, query):
    file_id = query.data.split("_")[1]
    try:
        user = await bot.get_chat_member(MAIN_CHANNEL, query.from_user.id)
        if user.status in ["member", "administrator", "creator"]:
            await bot.copy_message(chat_id=query.message.chat.id, from_chat_id=PRIVATE_CHANNEL_ID, message_id=int(file_id))
            await query.message.delete()
        else:
            await query.answer("❌ You haven't joined yet!", show_alert=True)
    except:
        await query.answer("Error checking membership.", show_alert=True)

# Admin file upload
@bot.on_message(filters.document | filters.video | filters.photo & filters.user(ADMIN_ID))
async def save_file(_, message):
    sent = await message.copy(chat_id=PRIVATE_CHANNEL_ID)
    file_link = f"https://t.me/{(await bot.get_me()).username}?start={sent.id}"
    await message.reply_text(
        f"✅ File Saved Successfully!\n\n🔗 Share Link:\n{file_link}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=file_link)]])
    )

print("Bot is running...")
bot.run()
