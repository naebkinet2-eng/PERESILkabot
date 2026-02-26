import telebot
import os
from flask import Flask
import threading

# 1. Вставь свой токен бота
TOKEN = '8795496069:AAFrxORXRroXihRI8IS8emZXXzX22U4drEM'

# 2. Укажи ID твоего канала или его юзернейм
CHANNEL_ID = '@SIOTZV123'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Заглушка для Render
@app.route('/')
def health_check():
    return "Bot is running and healthy!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Обработчик всех сообщений
@bot.message_handler(func=lambda message: message.chat.type == 'private', content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'animation'])
def forward_to_channel(message):
    try:
        # Используем forward_message вместо copy_message
        bot.forward_message(
            chat_id=CHANNEL_ID, 
            from_chat_id=message.chat.id, 
            message_id=message.message_id
        )
        bot.reply_to(message, "✅ Сообщение успешно переслано в канал.")
    except Exception as e:
        bot.reply_to(message, f"❌ Произошла ошибка. Текст ошибки: {e}")

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    print("Бот запущен...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
