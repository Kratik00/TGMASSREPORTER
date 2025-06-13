import os
import time
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, ConversationHandler
)
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import (
    InputReportReasonSpam, InputReportReasonFake, InputReportReasonOther
)
from config import BOT_TOKEN, API_ID, API_HASH

# States
LOGIN_PHONE, LOGIN_CODE, TARGET_USER, REPORT_COUNT, REPORT_REASON = range(5)

# /start with banner and promo buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📣 My Channel", url="https://t.me/URS_LUCIFER"),
            InlineKeyboardButton("👤 Contact Me", url="https://t.me/LP_LUCIFER")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo="https://graph.org/file/d1991cab84267f8c42e72-3834f7f3e6c18bb7b7.jpg",
        caption="👋 Welcome to TG Reporter Tool!\nType /help for commands\n\nStay connected with the developer:",
        reply_markup=reply_markup
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Available Commands:\n"
        "/start - Start the bot\n"
        "/login - Login with your Telegram number\n"
        "/report - Start mass reporting\n"
        "/logout - Delete saved session\n"
        "/cancel - Cancel current operation\n"
        "/help - Show this help message"
    )

# /login flow
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📩 Send your phone number (e.g. +91xxxx...):\nOr type /cancel to exit.")
    return LOGIN_PHONE

async def login_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    client = TelegramClient(f"sessions/{update.effective_user.id}", API_ID, API_HASH)
    await client.connect()
    await client.send_code_request(phone)
    context.user_data['client'] = client
    context.user_data['phone'] = phone
    await update.message.reply_text("🔑 OTP sent! Enter the code:\nOr type /cancel to exit.")
    return LOGIN_CODE

async def login_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text
    client = context.user_data['client']
    phone = context.user_data['phone']
    try:
        await client.sign_in(phone, code)
        await update.message.reply_text("✅ Login successful! Session saved.")
    except Exception as e:
        await update.message.reply_text(f"❌ Login failed: {e}")
    finally:
        await client.disconnect()
    return ConversationHandler.END

# /logout
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session_file = f"sessions/{update.effective_user.id}.session"
    if os.path.exists(session_file):
        os.remove(session_file)
        await update.message.reply_text("✅ Logged out and session removed.")
    else:
        await update.message.reply_text("⚠️ No session found to logout.")

# /report
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 Enter target username (without @):\nOr type /cancel to exit.")
    return TARGET_USER

async def get_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['target'] = update.message.text
    await update.message.reply_text("🔁 How many accounts to use?\nOr type /cancel to exit.")
    return REPORT_COUNT

async def get_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['count'] = int(update.message.text)
    except:
        await update.message.reply_text("❗ Please enter a valid number.")
        return REPORT_COUNT

    reply_markup = ReplyKeyboardMarkup([["spam", "fake", "other"]], one_time_keyboard=True)
    await update.message.reply_text("📝 Select report reason:", reply_markup=reply_markup)
    return REPORT_REASON

# Mass reporting - async coroutine per session
async def report_with_session(session_file, target_username, reason_obj, i, total):
    start = time.time()
    try:
        cli = TelegramClient(os.path.join("sessions", session_file), API_ID, API_HASH)
        await cli.start()

        res = await cli(ResolveUsernameRequest(target_username))

        await cli(ReportRequest(
            peer=res.users[0],
            id=[],
            reason=reason_obj,
            message="Reported via Telegram Bot"
        ))

        await cli.disconnect()
        end = time.time()
        return f"✅ Report {i}/{total} from `{session_file}` - ⏱️ {round(end - start, 2)}s"
    except Exception as e:
        end = time.time()
        return f"❌ Report {i}/{total} from `{session_file}` failed - {e} - ⏱️ {round(end - start, 2)}s"

# Run all reports in parallel
async def get_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reason = update.message.text.lower()
    if reason == "spam":
        reason_obj = InputReportReasonSpam()
    elif reason == "fake":
        reason_obj = InputReportReasonFake()
    else:
        reason_obj = InputReportReasonOther()

    sessions = sorted([f for f in os.listdir("sessions") if f.endswith(".session")])
    sessions = sessions[:context.user_data['count']]
    total = len(sessions)
    target_username = context.user_data['target']

    await update.message.reply_text(f"🚀 Starting parallel mass report on @{target_username} using {total} accounts...")

    tasks = [
        report_with_session(session_file, target_username, reason_obj, i+1, total)
        for i, session_file in enumerate(sessions)
    ]

    results = await asyncio.gather(*tasks)

    for result in results:
        await update.message.reply_text(result, parse_mode="Markdown")

    await update.message.reply_text("🎯 Mass reporting completed.")
    return ConversationHandler.END

# /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Operation cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Main bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("logout", logout))
    app.add_handler(CommandHandler("cancel", cancel))

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("login", login)],
        states={
            LOGIN_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_phone)],
            LOGIN_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_code)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    ))

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("report", report)],
        states={
            TARGET_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_target)],
            REPORT_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_count)],
            REPORT_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reason)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    ))

    print("🚀 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
