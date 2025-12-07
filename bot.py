import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest

BOT_TOKEN = "8279748377:AAFnf8irohjfmRn3tYyrYf9sqNgIUiGrPIA"
API_URL = "https://telegram-quiz-bot-pbts.onrender.com"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Online! 🚀")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f"{API_URL}/quiz")
    data = response.json()

    question = data["question"]
    options = data["options"]

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=opt)] for opt in options
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(question, reply_markup=reply_markup)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected = query.data

    response = requests.post(f"{API_URL}/check", json={"answer": selected})
    result = response.json()

    if result["correct"]:
        await query.edit_message_text("🎉 Correct Answer!")
    else:
        await query.edit_message_text("❌ Wrong Answer! Try again 😢")

req = HTTPXRequest(http_version="1.1")
app = ApplicationBuilder().token(BOT_TOKEN).request(req).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CallbackQueryHandler(handle_answer))

print("Bot Running...")
app.run_polling()
