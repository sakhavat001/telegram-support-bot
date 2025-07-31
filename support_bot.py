# -*- coding: utf-8 -*-
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")  # Railway-də gizli olaraq verəcəyik
bot = telebot.TeleBot(TOKEN)

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
        bot.send_message(call.message.chat.id, responses[call.data])

bot.polling()
