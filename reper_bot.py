import os
import time
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, ConversationHandler
)

from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import InputReportReasonSpam, InputReportReasonFake, InputReportReasonOther

from config import BOT_TOKEN, API_ID, API_HASH

# Dummy HTTP Server (for Koyeb / uptime)
class DummyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"TGReporter Bot Running")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_dummy_server():
    server = HTTPServer(('0.0.0.0', 8080), DummyServer)
    server.serve_forever()

# States
LOGIN_PHONE, LOGIN_CODE, TARGET_USER, REPORT_COUNT, REPORT_REASON = range(5)

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("\ud83d\udce3 My Channel", url="https://t.me/URS_LUCIFER"),
         InlineKeyboardButton("\ud83d\udc64 Contact Me", url="https://t.me/LP_LUCIFER")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo="https://graph.org/file/d1991cab84267f8c42e72-3834f7f3e6c18bb7b7.jpg",
        caption="\ud83d\udc4b Welcome to TG Reporter Tool!\nType /help for commands\n\nStay connected with the developer:",
        reply_markup=reply_markup
    )

# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "\ud83d\udee0 Available Commands:\n"
        "/start - Start the bot\n"
        "/login - Login with your Telegram number\n"
        "/report - Start mass reporting\n"
        "/logout - Delete saved session\n"
        "/cancel - Cancel current operation\n"
        "/help - Show this help message"
    )

# Login Flow
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\ud83d\udce9 Send your phone number (e.g. +91xxxx...):\nOr type /cancel to exit.")
    return LOGIN_PHONE

async def login_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    client = TelegramClient(f"sessions/{update.effective_user.id}", API_ID, API_HASH)
    await client.connect()
    await client.send_code_request(phone)
    context.user_data['client'] = client
    context.user_data['phone'] = phone
    await update.message.reply_text("\ud83d\udd11 OTP sent! Enter the code:\nOr type /cancel to exit.")
    return LOGIN_CODE

async def login_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text
    client = context.user_data['client']
    phone = context.user_data['phone']
    try:
        await client.sign_in(phone, code)
        await update.message.reply_text("\u2705 Login successful! Session saved.")
    except Exception as e:
        await update.message.reply_text(f"\u274c Login failed: {e}")
    finally:
        await client.disconnect()
    return ConversationHandler.END

# Logout
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session_file = f"sessions/{update.effective_user.id}.session"
    if os.path.exists(session_file):
        os.remove(session_file)
        await update.message.reply_text("\u2705 Logged out and session removed.")
    else:
        await update.message.reply_text("\u26a0\ufe0f No session found to logout.")

# Report
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session_path = f"sessions/{update.effective_user.id}.session"
    if not os.path.exists(session_path):
        await update.message.reply_text("\u2757 You're not logged in. Please use /login first.")
        return ConversationHandler.END

    await update.message.reply_text("\ud83c\udfaf Enter target username (without @):\nOr type /cancel to exit.")
    return TARGET_USER

async def get_target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['target'] = update.message.text
    await update.message.reply_text("\ud83d\udd01 How many accounts to use?\nOr type /cancel to exit.")
    return REPORT_COUNT

async def get_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['count'] = int(update.message.text)
    except:
        await update.message.reply_text("\u2757 Please enter a valid number.")
        return REPORT_COUNT

    reply_markup = ReplyKeyboardMarkup([["spam", "fake", "other"]], one_time_keyboard=True)
    await update.message.reply_text("\ud83d\uddd8\ufe0f Select report reason:", reply_markup=reply_markup)
    return REPORT_REASON

# Async reporting
async def report_with_session(session_file, target_username, reason_obj, i, total):
    start = time.time()
    try:
        cli = TelegramClient(os.path.join("sessions", session_file), API_ID, API_HASH)
        await cli.start()

        res = await asyncio.wait_for(cli(ResolveUsernameRequest(target_username)), timeout=10)
        await asyncio.wait_for(cli(ReportRequest(
            peer=res.users[0],
            id=[],
            reason=reason_obj,
            message="Reported via Telegram Bot"
        )), timeout=10)

        await cli.disconnect()
        end = time.time()
        return f"\u2705 Report {i}/{total} from `{session_file}` - \u23f1\ufe0f {round(end - start, 2)}s"
    except asyncio.TimeoutError:
        return f"\u274c Report {i}/{total} from `{session_file}` timed out"
    except Exception as e:
        end = time.time()
        return f"\u274c Report {i}/{total} from `{session_file}` failed - {e} - \u23f1\ufe0f {round(end - start, 2)}s"

# Final report runner
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

    await update.message.reply_text(f"\ud83d\ude80 Starting parallel mass report on @{target_username} using {total} accounts...")

    tasks = [
        report_with_session(session_file, target_username, reason_obj, i+1, total)
        for i, session_file in enumerate(sessions)
    ]

    results = await asyncio.gather(*tasks)

    for result in results:
        await update.message.reply_text(result, parse_mode="Markdown")

    await update.message.reply_text("\ud83c\udfaf Mass reporting completed.")
    return ConversationHandler.END

# Cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\u274c Operation cancelled.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Main

def main():
    threading.Thread(target=run_dummy_server, daemon=True).start()
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

    print("\ud83d\ude80 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
