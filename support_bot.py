# -*- coding: utf-8 -*-
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8318840240:AAGRrn3gzcdb5doSNf30v81YWmLlPn8_6S8'
bot = telebot.TeleBot(TOKEN)

# Menü düymələri
main_menu = InlineKeyboardMarkup(row_width=1)
main_menu.add(
    InlineKeyboardButton("📌 Haqqımızda", callback_data="about"),
    InlineKeyboardButton("📞 Əlaqə", callback_data="contact"),
    InlineKeyboardButton("🌐 Veb sayt", callback_data="website"),
    InlineKeyboardButton("🧪 Test 1", callback_data="test1"),
    InlineKeyboardButton("🧪 Test 2", callback_data="test2")
)

# Başlanğıc mesajı
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Salam! Aşağıdakı mövzulardan birini seçin:",
        reply_markup=main_menu
    )

# Callback funksiyası — düymə kliklənəndə cavab verilir
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "about":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Biz IT ilə bağlı bütün xidmətləri göstəririk.")
    elif call.data == "contact":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Əlaqə nömrəmiz: +994 51 111 11 11")
    elif call.data == "website":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Veb saytların hazırlanması 300 AZN-dən başlayır.")
    elif call.data == "test1":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Test 1 cavabıdır.")
    elif call.data == "test2":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Test 2 cavabıdır.")

bot.polling()