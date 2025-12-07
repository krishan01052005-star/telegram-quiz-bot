from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8279748377:AAG25G_FKfbdwh7WkZGbNXAHaz1JoR90MwQ"

questions = [
    {"q": "भारत की राजधानी क्या है?", "a": "B"},
    {"q": "मोबाइल का फुल फॉर्म?", "a": "C"},
    {"q": "CPU का फुल फॉर्म?", "a": "A"}
]

options = [
    ["A) मुंबई", "B) नई दिल्ली", "C) कोलकाता"],
    ["A) Mini Phone", "B) Mobile Box", "C) Mobile International"],
    ["A) Central Processing Unit", "B) Computer Main Unit", "C) Control Processing Utility"]
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("नमस्ते! मैं Quiz Bot हूँ 😊\n/quiz लिखकर क्विज शुरू करें")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.id
    user_data[user] = 0
    await ask_question(update, context)

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.id
    qid = user_data[user]

    if qid < len(questions):
        question = questions[qid]
        reply_markup = ReplyKeyboardMarkup([["A", "B", "C"]], one_time_keyboard=True)
        await update.message.reply_text(f"Q{qid+1}: {question['q']}\n\n"
                                        + "\n".join(options[qid]),
                                        reply_markup=reply_markup)
    else:
        await update.message.reply_text("🎉 क्विज खत्म!\n👍 धन्यवाद खेल खेलने के लिए!")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.id
    if user not in user_data:
        await update.message.reply_text("पहले /quiz भेजें!")
        return

    qid = user_data[user]
    correct = questions[qid]["a"]

    if update.message.text.upper() == correct:
        await update.message.reply_text("✔️ सही जवाब!")
    else:
        await update.message.reply_text(f"❌ गलत!\nसही जवाब: {correct}")

    user_data[user] += 1
    await ask_question(update, context)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), answer))

    print("🤖 Bot Started... Telegram Me /start bhejo")
    app.run_polling()
