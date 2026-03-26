import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Твой токен и ссылка на Mini App
TOKEN = "8768303694:AAFEDa4lOHFHX439A7vcfh2qGltZciQBYXE"
WEB_APP_URL = "https://ltt.wuaze.com/?i=1"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    # Создаем кнопки как на скриншоте
    kb = [
        [
            # Кнопка Mini App (открывает твой сайт внутри Телеграм)
            InlineKeyboardButton(
                text="📲 КУПИТЬ (с vpn)", 
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ],
        [
            InlineKeyboardButton(text="💼 РАБОТА", callback_data="btn_work"),
            InlineKeyboardButton(text="💳 ПРОФИЛЬ", callback_data="btn_profile")
        ],
        [
            InlineKeyboardButton(text="ПРАВИЛА", callback_data="btn_rules"),
            InlineKeyboardButton(text="ИНФОРМАЦИЯ", callback_data="btn_info")
        ],
        [
            InlineKeyboardButton(text="🔔 ОПОВЕЩЕНИЯ", callback_data="btn_notif")
        ],
        [
            InlineKeyboardButton(text="ОПЕРАТОР ↗️", callback_data="btn_operator")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Текст сообщения в точности как на скрине
    welcome_text = (
        "Добро пожаловать в магазин ❤️ Love Store!\n\n"
        "🐱 Наш магазин представлен на популярных площадках, таких как "
        "Kr**en, Me*a, Bla*kSp*ut и проверен более чем 10.000 заказами наших довольных клиентов\n\n"
        "Работаем в большинстве городов РФ\n"
        "Наш оператор доступен для вас 24/7, в случае возникновения вопросов "
        "или спорных ситуаций мы ответим вам в течение 30 минут!\n\n"
        "💼 У нас открыты вакансии, требуются:\n"
        "Курьеры, водители меж-город, трафаретчики во всех городах!\n"
        "За подробностями обращайтесь к оператору 👇\n"
        "❄️ Платим дох*я! ❄️\n\n"
        "🐱 АКТУАЛЬНЫЕ КОНТАКТЫ\n"
        "Оператор тг: @OperatorLoveStore\n"
        "Бот-оповещатель: t.me/LoveStoreOpoBot\n"
        "Канал информации: t.me/InfoLoveStore\n\n"
        "❤️ Приятных покупок в LoveStore ❤️\n\n"
        "📱 Больше функционала в ПРИЛОЖЕНИИ 📱"
    )
    
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

# Обработчик нажатий на остальные кнопки (заглушка)
@dp.callback_query(F.data.startswith("btn_"))
async def callbacks_handler(callback: types.CallbackQuery):
    await callback.answer("Раздел в разработке или пуст", show_alert=False)

async def main():
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
