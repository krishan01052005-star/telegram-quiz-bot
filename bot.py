import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest

BOT_TOKEN = "8279748377:AAFnf8irohjfmRn3tYyrYf9sqNgIUiGrPIA"
API_URL = "http://127.0.0.1:5000"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Online! 🚀")

req = HTTPXRequest(http_version="1.1")

app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .request(req)
    .build()
)

app.add_handler(CommandHandler("start", start))

print("Bot Running...")
app.run_polling()
