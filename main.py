import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

TOKEN = "8768303694:AAFEDa4lOHFHX439A7vcfh2qGltZciQBYXE"
WEB_APP_URL = "https://ltt.wuaze.com/?i=1"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Веб-сервер для Render ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render сам подставляет порт в переменную окружения PORT
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# --- Логика бота (та же, что была раньше) ---
def get_main_keyboard():
    kb = [
        [InlineKeyboardButton(text="📲 КУПИТЬ (с vpn)", web_app=WebAppInfo(url=WEB_APP_URL))],
        [InlineKeyboardButton(text="💼 РАБОТА", callback_data="btn_work"),
         InlineKeyboardButton(text="💳 ПРОФИЛЬ", callback_data="btn_profile")],
        [InlineKeyboardButton(text="ПРАВИЛА", callback_data="btn_rules"),
         InlineKeyboardButton(text="ИНФОРМАЦИЯ", callback_data="btn_info")],
        [InlineKeyboardButton(text="🔔 ОПОВЕЩЕНИЯ", callback_data="btn_notif")],
        [InlineKeyboardButton(text="ОПЕРАТОР ↗️", callback_data="btn_operator")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    welcome_text = "Добро пожаловать в магазин ❤️ Love Store! ..." # Твой текст
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.callback_query(F.data.startswith("btn_"))
async def callbacks_handler(callback: types.CallbackQuery):
    await callback.answer("Раздел в разработке", show_alert=False)

async def main():
    # Запускаем веб-сервер и бота одновременно
    await start_web_server()
    print("Бот и Веб-сервер запущены!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
