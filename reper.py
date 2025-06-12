import os
import asyncio
import argparse
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.errors import SessionPasswordNeededError
from colorama import Fore, Style, init

init(autoreset=True)

# === Replace with your actual API credentials ===
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'

# === Argument Parser ===
parser = argparse.ArgumentParser()
parser.add_argument("-an", "--add_number", help="Add Telegram session by phone number")
parser.add_argument("-t", "--target", help="Username of user to report")
parser.add_argument("-r", "--repeat", type=int, help="Number of times to report")
parser.add_argument("-m", "--mode", default="spam", help="Report mode: spam, violence, etc.")
args = parser.parse_args()

# === Report Reason Mapping ===
reason_map = {
    "spam": types.InputReportReasonSpam(),
    "violence": types.InputReportReasonViolence(),
    "child_abuse": types.InputReportReasonChildAbuse(),
    "pornography": types.InputReportReasonPornography(),
    "fake": types.InputReportReasonFake(),
    "illegal_drugs": types.InputReportReasonIllegalDrugs(),
    "copyright": types.InputReportReasonCopyright(),
    "geo_irrelevant": types.InputReportReasonGeoIrrelevant()
}

def show_banner():
    print(Style.BRIGHT + Fore.RED + "\n" + "═" * 90)

    # TRIPLE SIZE TGREPORTER
    tgrep = [
        Fore.RED + "T",
        Fore.YELLOW + "G",
        Fore.GREEN + "R",
        Fore.CYAN + "E",
        Fore.MAGENTA + "P",
        Fore.BLUE + "O",
        Fore.LIGHTYELLOW_EX + "R",
        Fore.LIGHTMAGENTA_EX + "T",
        Fore.LIGHTCYAN_EX + "E",
        Fore.LIGHTRED_EX + "R"
    ]
    tg_line = "  ".join(tgrep)
    print(f"{Style.BRIGHT}{tg_line.center(90)} {Fore.LIGHTGREEN_EX}🔰")

    # Subtitle
    print(Fore.LIGHTCYAN_EX + "Telegram Mass Reporter Tool".center(90))
    print(Fore.LIGHTMAGENTA_EX + "Built with ❤️ by @LP_LUCIFER".center(90))

    # GitHub with pink + yellow
    print(Fore.LIGHTMAGENTA_EX + "GitHub: " + Fore.YELLOW + "https://github.com/LP-LUCIFER".center(83))
    print(Fore.RED + "═" * 90 + Style.RESET_ALL + "\n")
async def add_account(phone):
    client = TelegramClient(phone, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            code = input("[?] Enter the code sent to {}: ".format(phone))
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            pw = input("[?] 2FA Password: ")
            await client.sign_in(password=pw)
    await client.disconnect()
    print(f"[+] Session for {phone} created successfully.")

async def report_user(target, reason_key, repeat):
    if reason_key not in reason_map:
        print(f"[!] Unknown reason '{reason_key}'. Using 'spam' by default.")
        reason = types.InputReportReasonSpam()
    else:
        reason = reason_map[reason_key]

    sessions = [f for f in os.listdir('.') if f.endswith('.session')]

    if not sessions:
        print("[!] No session files found.")
        return

    for i in range(repeat):
        for ses in sessions:
            try:
                client = TelegramClient(ses.replace('.session', ''), api_id, api_hash)
                await client.start()
                entity = await client.get_entity(target)
                await client(functions.account.ReportPeerRequest(
                    peer=entity,
                    reason=reason,
                    message="Reported via Lucifer TGReporter"
                ))
                print(f"[{i+1}] Report sent using {ses}")
                await asyncio.sleep(1)
                await client.disconnect()
            except Exception as e:
                print(f"[!] Failed with session {ses}: {e}")

async def main():
    show_banner()
    if args.add_number:
        await add_account(args.add_number)
    elif args.target:
        await report_user(args.target, args.mode, args.repeat or 1)
    else:
        print("Usage:")
        print("  Add session: python3 reper.py -an +1234567890")
        print("  Report user: python3 reper.py -t target_username -r 100 -m spam")

if __name__ == '__main__':
    asyncio.run(main())
