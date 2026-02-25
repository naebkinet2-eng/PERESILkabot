import telebot
import os
from flask import Flask
import threading

# 1. Вставь свой токен бота в кавычки ниже:
TOKEN = '8795496069:AAFrxORXRroXihRI8IS8emZXXzX22U4drEM'

CHANNEL_ID = '8125791280'

# Инициализируем бота и веб-сервер
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Заглушка для Render, чтобы он видел рабочий веб-сервис
@app.route('/')
def health_check():
    return "Bot is running and healthy!"

def run_flask():
    # Render сам выдает порт через переменные окружения
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Обработчик всех сообщений, которые присылают боту в личку
@bot.message_handler(func=lambda message: message.chat.type == 'private', content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'animation'])
def forward_to_channel(message):
    try:
        # copy_message копирует сообщение без плашки "Переслано от..." 
        # Если нужна плашка, используй bot.forward_message(...)
        bot.copy_message(
            chat_id=CHANNEL_ID, 
            from_chat_id=message.chat.id, 
            message_id=message.message_id
        )
        bot.reply_to(message, "✅ Сообщение успешно отправлено в канал.")
    except Exception as e:
        bot.reply_to(message, f"❌ Произошла ошибка: Скорее всего бот не админ в канале. Текст ошибки: {e}")

if __name__ == "__main__":
    # 1. Запускаем Flask-сервер в отдельном потоке (решает проблему с выключением на Render)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # 2. Запускаем самого бота
    print("Бот запущен...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
