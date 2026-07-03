import json
from telegram import Bot
from datetime import datetime

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL = "@Amiran_fooladnovin"

INSTAGRAM = "https://instagram.com/AMIRAN_FOOLADNV"
CHANNEL_LINK = "https://t.me/Amiran_fooladnovin"

def load_prices():
    with open("prices.json", "r", encoding="utf-8") as f:
        return json.load(f)

def send_prices():
    bot = Bot(token=TOKEN)
    data = load_prices()

    today = datetime.now().strftime("%Y/%m/%d")

    # 📌 سپری
    sepri_text = f"""
🏭 نورد امیران فولاد

📅 تاریخ: {today}

📌 قیمت سپری:
🔹 3 : {data['sepri3']}
🔹 4 : {data['sepri4']}
🔹 5 : {data['sepri5']}
🔹 6 : {data['sepri6']}

━━━━━━━━━━━━━━━
📸 اینستاگرام: {INSTAGRAM}
🔗 کانال: {CHANNEL_LINK}
"""

    # 📌 میلگرد
    rebar_text = f"""
🏭 نورد امیران فولاد

📅 تاریخ: {today}

📌 قیمت میلگرد:
🔸 14 : {data['rebar14']}
🔸 16 : {data['rebar16']}
🔸 18 : {data['rebar18']}
🔸 20 : {data['rebar20']}
🔸 22 : {data['rebar22']}
🔸 25 : {data['rebar25']}
🔸 28 : {data['rebar28']}
🔸 32 : {data['rebar32']}

━━━━━━━━━━━━━━━
📸 اینستاگرام: {INSTAGRAM}
🔗 کانال: {CHANNEL_LINK}
"""

    bot.send_message(chat_id=CHANNEL, text=sepri_text)
    bot.send_message(chat_id=CHANNEL, text=rebar_text)


send_prices()
