# ==========================
# PART 1 / 10
# Webhook Version (Render)
# ==========================

import os
import json
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==========================
# تنظیمات
# ==========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

PORT = int(
    os.getenv(
        "PORT",
        10000
    )
)

CHANNEL_ID = "@Amiran_fooladnovin"

ADMIN_ID = 123456789
# ← اینجا آی دی عددی خودت

INSTAGRAM_URL = "https://instagram.com/AMIRAN_FOOLADNV"

CHANNEL_URL = "https://t.me/Amiran_foolad"

PRICE_FILE = "prices.json"

# ==========================
# لاگ
# ==========================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)

# ==========================
# وضعیت کاربران
# ==========================

user_state = {}

# ==========================
# ساخت فایل قیمت
# ==========================

def ensure_price_file():

    if not os.path.exists(PRICE_FILE):

        with open(

            PRICE_FILE,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                {},

                f,

                ensure_ascii=False,

                indent=4

            )

# ==========================
# خواندن قیمت
# ==========================

def load_prices():

    ensure_price_file()

    try:

        with open(

            PRICE_FILE,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    except Exception:

        return {}

# ==========================
# ذخیره قیمت
# ==========================

def save_prices(data):

    with open(

        PRICE_FILE,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            data,

            f,

            ensure_ascii=False,

            indent=4

        )

# ==========================
# بررسی ادمین
# ==========================

def is_admin(user_id):

    return user_id == ADMIN_ID

# ==========================
# استارت
# ==========================

async def start(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    if not is_admin(

        update.effective_user.id

    ):

        await update.message.reply_text(

            "⛔ دسترسی ندارید."

        )

        return

    keyboard = [

        [

            InlineKeyboardButton(

                "📦 پنل مدیریت",

                callback_data="panel"

            )

        ]

    ]

    await update.message.reply_text(

        "✅ ربات آماده است.",

        reply_markup=InlineKeyboardMarkup(

            keyboard

        )

    )
    # ==========================
# PART 2 / 10
# پنل مدیریت
# ==========================

async def panel(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    if not is_admin(

        query.from_user.id

    ):

        return

    keyboard = [

        [

            InlineKeyboardButton(

                "📦 سپری",

                callback_data="product_sepri"

            )

        ],

        [

            InlineKeyboardButton(

                "🏗 میلگرد",

                callback_data="product_rebar"

            )

        ],

        [

            InlineKeyboardButton(

                "📤 ارسال قیمت ها",

                callback_data="send_prices"

            )

        ],

        [

            InlineKeyboardButton(

                "📊 مشاهده قیمت ها",

                callback_data="show_prices"

            )

        ],

        [

            InlineKeyboardButton(

                "📢 کانال",

                url=CHANNEL_URL

            ),

            InlineKeyboardButton(

                "📸 اینستاگرام",

                url=INSTAGRAM_URL

            )

        ]

    ]

    await query.edit_message_text(

        "پنل مدیریت امیران فولاد",

        reply_markup=InlineKeyboardMarkup(

            keyboard

        )

    )

# ==========================
# انتخاب محصول
# ==========================

async def select_product(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    product = query.data.replace(

        "product_",

        ""

    )

    user_state[

        query.from_user.id

    ] = {

        "product": product

    }

    if product == "sepri":

        sizes = [

            "3",

            "4",

            "5",

            "6"

        ]

    else:

        sizes = [

            "14",

            "16",

            "18",

            "20",

            "22",

            "25",

            "28",

            "32"

        ]

    keyboard = []

    for size in sizes:

        keyboard.append(

            [

                InlineKeyboardButton(

                    size,

                    callback_data=f"size_{size}"

                )

            ]

        )

    keyboard.append(

        [

            InlineKeyboardButton(

                "⬅ بازگشت",

                callback_data="panel"

            )

        ]

    )

    await query.edit_message_text(

        "سایز موردنظر را انتخاب کن.",

        reply_markup=InlineKeyboardMarkup(

            keyboard

        )

    )

# ==========================
# انتخاب سایز
# ==========================

async def select_size(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    size = query.data.replace(

        "size_",

        ""

    )

    if user_id not in user_state:

        user_state[user_id] = {}

    user_state[user_id][

        "size"

    ] = size

    await query.message.reply_text(

        "💰 قیمت را فقط به صورت عدد ارسال کن."

        )
    # ==========================
# PART 3 / 10
# ثبت قیمت
# ==========================

async def handle_price(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    user_id = update.effective_user.id

    if not is_admin(user_id):

        return

    if user_id not in user_state:

        await update.message.reply_text(

            "ابتدا محصول را انتخاب کن."

        )

        return

    if "product" not in user_state[user_id]:

        await update.message.reply_text(

            "ابتدا محصول را انتخاب کن."

        )

        return

    if "size" not in user_state[user_id]:

        await update.message.reply_text(

            "ابتدا سایز را انتخاب کن."

        )

        return

    price = update.message.text.strip()

    if not price.isdigit():

        await update.message.reply_text(

            "❌ فقط عدد وارد کن."

        )

        return

    product = user_state[user_id]["product"]

    size = user_state[user_id]["size"]

    prices = load_prices()

    prices[f"{product}_{size}"] = price

    save_prices(prices)

    user_state[user_id] = {}

    await update.message.reply_text(

        "✅ قیمت با موفقیت ثبت شد."

    )

# ==========================
# ساخت متن سپری
# ==========================

def build_sepri_message():

    prices = load_prices()

    text = "📦 قیمت سپری\n\n"

    for size in [

        "3",

        "4",

        "5",

        "6"

    ]:

        value = prices.get(

            f"sepri_{size}",

            "---"

        )

        text += (

            f"سپری {size} : "

            f"{value}\n"

        )

    return text

# ==========================
# ساخت متن میلگرد
# ==========================

def build_rebar_message():

    prices = load_prices()

    text = "🏗 قیمت میلگرد\n\n"

    for size in [

        "14",

        "16",

        "18",

        "20",

        "22",

        "25",

        "28",

        "32"

    ]:

        value = prices.get(

            f"rebar_{size}",

            "---"

        )

        text += (

            f"میلگرد {size} : "

            f"{value}\n"

        )

    return text
    # ==========================
# PART 4 / 10
# ارسال قیمت ها
# ==========================

async def send_prices(

    context: ContextTypes.DEFAULT_TYPE

):

    try:

        keyboard = [

            [

                InlineKeyboardButton(

                    "📢 کانال تلگرام",

                    url=CHANNEL_URL

                )

            ],

            [

                InlineKeyboardButton(

                    "📸 اینستاگرام",

                    url=INSTAGRAM_URL

                )

            ]

        ]

        markup = InlineKeyboardMarkup(

            keyboard

        )

        await context.bot.send_message(

            chat_id=CHANNEL_ID,

            text=build_sepri_message(),

            reply_markup=markup

        )

        await context.bot.send_message(

            chat_id=CHANNEL_ID,

            text=build_rebar_message(),

            reply_markup=markup

        )

        logger.info(

            "Prices Sent Successfully"

        )

    except Exception as e:

        logger.error(e)

# ==========================
# ارسال دستی
# ==========================

async def manual_send(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    if not is_admin(

        query.from_user.id

    ):

        return

    await send_prices(

        context

    )

    await query.message.reply_text(

        "✅ قیمت ها ارسال شدند."

    )

# ==========================
# مشاهده قیمت ها
# ==========================

async def show_prices(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    await query.answer()

    if not is_admin(

        query.from_user.id

    ):

        return

    await query.message.reply_text(

        build_sepri_message()

    )

    await query.message.reply_text(

        build_rebar_message()

)
    # ==========================
# PART 5 / 10
# Callback ها
# ==========================

async def callback_handler(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    query = update.callback_query

    data = query.data

    if data == "panel":

        await panel(

            update,

            context

        )

        return

    if data == "send_prices":

        await manual_send(

            update,

            context

        )

        return

    if data == "show_prices":

        await show_prices(

            update,

            context

        )

        return

    if data.startswith(

        "product_"

    ):

        await select_product(

            update
            # ==========================
# PART 6 / 10
# ساخت برنامه
# ==========================

def create_application():

    app = Application.builder().token(

        BOT_TOKEN

    ).build()

    # -----------------------
    # Command ها
    # -----------------------

    app.add_handler(

        CommandHandler(

            "start",

            start

        )

    )

    app.add_handler(

        CommandHandler(

            "status",

            status

        )

    )

    app.add_handler(

        CommandHandler(

            "cancel",

            cancel

        )

    )

    # -----------------------
    # Callback ها
    # -----------------------

    app.add_handler(

        CallbackQueryHandler(

            callback_handler

        )

    )

    # -----------------------
    # ثبت قیمت
    # -----------------------

    app.add_handler(

        MessageHandler(

            filters.TEXT
            & ~filters.COMMAND,

            handle_price

        )

    )

    # -----------------------
    # Error Handler
    # -----------------------

    app.add_error_handler(

        error_handler

    )

    return app


# ==========================
# زمان بندی
# ==========================

def setup_jobs(app):

    if app.job_queue:

        app.job_queue.run_daily(

            send_prices,

            time=time(

                hour=21,

                minute=0

            ),

            name="daily_prices"

        )


# ==========================
# آماده سازی
# ==========================

def initialize(app):

    ensure_price_file()

    setup_jobs(app)

    logger.info(

        "Initialization Completed."

    )
    # ==========================
# PART 7 / 10
# اجرای ربات (Polling)
# ==========================

def main():

    logger.info(

        "Starting Bot..."

    )

    app = create_application()

    initialize(app)

    logger.info(

        "Bot Started Successfully."

    )

    app.run_polling(

        allowed_updates=Update.ALL_TYPES,

        drop_pending_updates=True

    )


# ==========================
# اجرای فایل
# ==========================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        logger.info(

            "Bot Stopped."

        )

    except Exception as e:

        logger.exception(e)
        # ==========================
# PART 8 / 10
# دستورات مدیریتی
# ==========================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_admin(update.effective_user.id):
        return

    text = """
📌 دستورات ربات

/start
نمایش پنل

/status
وضعیت ربات

/cancel
لغو عملیات

/help
راهنما
"""

    await update.message.reply_text(text)


# ==========================
# بکاپ قیمت ها
# ==========================

def backup_prices():

    prices = load_prices()

    with open(
        "prices_backup.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            prices,
            f,
            ensure_ascii=False,
            indent=4
        )


# ==========================
# بازیابی بکاپ
# ==========================

def restore_prices():

    if not os.path.exists(
        "prices_backup.json"
    ):
        return

    with open(
        "prices_backup.json",
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    save_prices(data)


# ==========================
# ذخیره امن
# ==========================

def safe_save(data):

    save_prices(data)

    backup_prices()


# ==========================
# بررسی فایل قیمت
# ==========================

def check_prices():

    try:

        ensure_price_file()

        load_prices()

    except Exception:

        restore_prices()
        # ==========================
# PART 9 / 10
# ثبت Handler ها
# ==========================

def register_handlers(app):

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "status",
            status
        )
    )

    app.add_handler(
        CommandHandler(
            "cancel",
            cancel
        )
    )

    app.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            callback_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_price
        )
    )

    app.add_error_handler(
        error_handler
    )

# ==========================
# آماده سازی کامل
# ==========================

def initialize_bot(app):

    ensure_price_file()

    check_prices()

    setup_jobs(app)

    register_handlers(app)

    logger.info(
        "Bot Initialized Successfully."
    )

# ==========================
# بررسی تنظیمات
# ==========================

def check_config():

    if not BOT_TOKEN:

        raise RuntimeError(
            "BOT_TOKEN تنظیم نشده است."
        )

    if ADMIN_ID == 123456789:

        logger.warning(
            "ADMIN_ID را تغییر نداده ای."
        )

    logger.info(
        "Configuration Loaded."
    )
    # ==========================
# PART 10 / 10
# اجرای نهایی
# ==========================

def main():

    check_config()

    app = create_application()

    register_handlers(app)

    initialize_bot(app)

    logger.info(

        "Bot Started Successfully."

    )

    app.run_polling(

        drop_pending_updates=True,

        allowed_updates=Update.ALL_TYPES

    )


# ==========================
# اجرای برنامه
# ==========================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        logger.info(

            "Bot Stopped."

        )

    except Exception as e:

        logger.exception(e)
