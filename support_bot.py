# -*- coding: utf-8 -*-
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Operatorun Telegram chat ID-sini daxil edin
OPERATOR_CHAT_ID = 123456789  # Buraya öz operator chat ID-nizi yazın

main_menu = InlineKeyboardMarkup(row_width=1)
main_menu.add(
    InlineKeyboardButton("📌 Haqqımızda", callback_data="about"),
    InlineKeyboardButton("📞 Əlaqə", callback_data="contact"),
    InlineKeyboardButton("🌐 Veb sayt", callback_data="website")
)

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Salam! Aşağıdakı mövzulardan birini seçin:",
        reply_markup=main_menu
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    responses = {
        "about": "Biz IT ilə bağlı bütün xidmətləri göstəririk.",
        "contact": "Əlaqə nömrəsi: +994 51 111 11 11",
        "website": "Veb sayt hazırlanması 300 AZN-dən başlayır."
    }
    if call.data in responses:
        bot.answer_callback_query(call.id)

        # Əvvəlki mesajı silirik
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as e:
            print(f"Mesajı silmək mümkün olmadı: {e}")

        # Yeni mesajı göndəririk
        bot.send_message(call.message.chat.id, responses[call.data])

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.chat.id != OPERATOR_CHAT_ID:
        # Müştəri mesajını operatora göndəririk
        forward_text = (
            f"👤 Müştəri (@{message.from_user.username}):\n"
            f"{message.text}\n"
            f"Chat ID: {message.chat.id}"
        )
        bot.send_message(OPERATOR_CHAT_ID, forward_text)
    else:
        # Operator mesajlarını qəbul edirik
        if message.text.startswith('/reply'):
            parts = message.text.split(' ', 2)
            if len(parts) < 3:
                bot.send_message(OPERATOR_CHAT_ID, "İstifadə: /reply <chat_id> <mesaj>")
                return
            try:
                target_chat_id = int(parts[1])
            except ValueError:
                bot.send_message(OPERATOR_CHAT_ID, "Chat ID düzgün deyil.")
                return
            reply_text = parts[2]
            bot.send_message(target_chat_id, f"Operatordan: {reply_text}")
        else:
            bot.send_message(OPERATOR_CHAT_ID, "Naməlum əməliyyat. Cavab üçün: /reply <chat_id> <mesaj>")

bot.polling()
