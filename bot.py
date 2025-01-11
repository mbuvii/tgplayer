import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN
from utils.youtube_handler import search_youtube, download_youtube

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Send me a song name and I'll search YouTube for it.\n"
        "You can then choose to download it as audio or video."
    )

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    results = await search_youtube(query)
    
    if not results:
        await update.message.reply_text("Sorry, no results found!")
        return

    keyboard = []
    for result in results:
        keyboard.append([
            InlineKeyboardButton(
                result['title'][:50] + "...",
                callback_data=f"select_{result['id']}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select a song:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("select_"):
        video_id = query.data.split("_")[1]
        keyboard = [
            [
                InlineKeyboardButton("Audio (128kbps)", callback_data=f"dl_audio_{video_id}_128"),
                InlineKeyboardButton("Audio (320kbps)", callback_data=f"dl_audio_{video_id}_320")
            ],
            [
                InlineKeyboardButton("Video (360p)", callback_data=f"dl_video_{video_id}_360"),
                InlineKeyboardButton("Video (720p)", callback_data=f"dl_video_{video_id}_720")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Choose format:", reply_markup=reply_markup)

    elif query.data.startswith("dl_"):
        _, type_, video_id, quality = query.data.split("_")
        await query.edit_message_text("⏳ Downloading... Please wait.")
        
        try:
            file_path = await download_youtube(video_id, type_, quality)
            if type_ == "audio":
                await query.message.reply_audio(audio=open(file_path, 'rb'))
            else:
                await query.message.reply_video(video=open(file_path, 'rb'))
            os.remove(file_path)  # Clean up after sending
        except Exception as e:
            await query.message.reply_text(f"Sorry, an error occurred: {str(e)}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
