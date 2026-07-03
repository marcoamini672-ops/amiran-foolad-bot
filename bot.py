import json
from datetime import datetime

from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================== تنظیمات ==================
TOKEN = "8882685860:AAEaRbNLhzUDsOzNvH9B0Sb-vCtX6po8Xeo"  
CHANNEL = "@Amiran_fooladnovin"
ADMIN_ID = "@Amiran_foolad"

INSTAGRAM = "https://instagram.com/AMIRAN_FOOLADNV"
CHANNEL_LINK = "https://t.me/Amiran_foolad"

user_state = {}

bot = Bot(token=TOKEN)

# ================== فایل قیمت ==================
def load_prices():
    with open("prices.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_prices(data):
    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ================== پنل ادمین ==================
async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    keyboard = [
        [InlineKeyboardButton("📦 سپری", callback_data="sepri")],
        [InlineKeyboardButton("🏗 میلگرد", callback_data="rebar")]
    ]

    await update.message.reply_text(
        "📌 محصول رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================== انتخاب محصول ==================
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_state[query.from_user.id] = {"product": query.data}

    if query.data == "sepri":
        sizes = ["3", "4", "5", "6"]
    else:
        sizes = ["14", "16", "18", "20", "22", "25", "28", "32"]

    keyboard = [[InlineKeyboardButton(s, callback_data=f"size_{s}")] for s in sizes]

    await query.message.reply_text(
        "📏 سایز رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================== انتخاب سایز ==================
async def size_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    size = query.data.replace("size_", "")
    user_state[query.from_user.id]["size"] = size

    await query.message.reply_text("💰 قیمت رو فقط عدد بفرست")

# ================== ذخیره قیمت ==================
async def handle_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        return

    if user_id not in user_state:
        return

    price = update.message.text

    product = user_state[user_id]["product"]
    size = user_state[user_id]["size"]

    key = f"{product}{size}"

    data = load_prices()
    data[key] = price
    save_prices(data)

    await update.message.reply_text("✔ قیمت ثبت شد")

# ================== اجرا ==================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("panel", panel))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CallbackQueryHandler(size_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_price))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
