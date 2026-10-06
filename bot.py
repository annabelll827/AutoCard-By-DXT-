import random
import string
import os
import telebot
from dotenv import load_dotenv

# بارکردنی فایلی .env
load_dotenv()

# خوێندنەوەی تۆکن لە فایلی .envەوە بە سەلامەتی
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

FILENAME = "mixed_scratch_codes.txt"

def load_existing_codes():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def generate_mixed_card_code():
    used_codes = load_existing_codes()
    characters = string.ascii_uppercase + string.digits
    
    while True:
        raw_code = ''.join(random.choice(characters) for _ in range(12))
        formatted_code = f"{raw_code[0:4]}-{raw_code[4:8]}-{raw_code[8:12]}"
        
        if formatted_code not in used_codes:
            with open(FILENAME, "a") as f:
                f.write(formatted_code + "\n")
            return formatted_code

@bot.message_handler(commands=['start', 'code'])
def send_code(message):
    new_code = generate_mixed_card_code()
    ussd_code = f"*221*{new_code}#"
    
    response_text = (
        f"🎟 **کۆدی نوێی کارتەکەت:**\n\n"
        f"`{ussd_code}`\n\n"
        f"📋 کۆدەکە کۆپی بکە و لە موبایلەکەت لێیدە!"
    )
    
    bot.reply_to(message, response_text, parse_mode="Markdown")

if __name__ == "__main__":
    print("بۆتەکە بە سەلامەتی کار دەکات...")
    bot.polling()
