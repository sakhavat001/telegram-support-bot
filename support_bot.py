# -*- coding: utf-8 -*-
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Token mühit dəyişənindən (Railway üçün)
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Telegram qrupunun chat ID-si → BURANI DƏYİŞİN
GROUP_CHAT_ID = -1002636527214  # <-- Öz qrupunuzun chat ID-sini bura yazın

# Menyu düymələri
main_menu = InlineKeyboardMarkup(row_width=1)
main_menu.add(
    InlineKeyboardButton("📌 Haqqımızda", callback_data="about"),
    InlineKeyboardButton("📞 Əlaqə", callback_data="contact"),
    InlineKeyboardButton("🌐 Veb sayt", callback_data="website")
)

# /start və /menu komandası
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Salam! Aşağıdakı mövzulardan birini seçin:",
        reply_markup=main_menu
    )

# Menyu seçimlərinə cavab
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "about":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Biz IT ilə bağlı bütün xidmətləri göstəririk.")
    
    elif call.data == "website":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Veb sayt hazırlanması 300 AZN-dən başlayır.")
    
    elif call.data == "contact":
        bot.answer_callback_query(call.id)
        
        # Qrupa bildiriş göndərilir
        group_text = (
            f"📞 Yeni əlaqə istəyi!\n"
            f"👤 @{call.from_user.username or 'Ad yoxdur'}\n"
            f"🆔 Chat ID: {call.message.chat.id}"
        )
        bot.send_message(GROUP_CHAT_ID, group_text)
        
        # İstifadəçiyə məlumat verilir
        bot.send_message(call.message.chat.id, "✅ Operator sizinlə tezliklə əlaqə saxlayacaq.")

# Operator cavabları üçün handler
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.chat.id == GROUP_CHAT_ID:
        # Qrupdan yazılan cavablar üçün
        if message.text.startswith('/reply'):
            parts = message.text.split(' ', 2)
            if len(parts) < 3:
                bot.send_message(GROUP_CHAT_ID, "İstifadə: /reply <chat_id> <mesaj>")
                return
            try:
                target_chat_id = int(parts[1])
            except ValueError:
                bot.send_message(GROUP_CHAT_ID, "Chat ID düzgün deyil.")
                return
            reply_text = parts[2]
            bot.send_message(target_chat_id, f"👨‍💼 Operator: {reply_text}")
        else:
            bot.send_message(GROUP_CHAT_ID, "Cavab üçün: /reply <chat_id> <mesaj>")
    else:
        # İstifadəçi mesajı qrupda operatorlara yönləndirilir
        forward_text = (
            f"📩 Yeni mesaj:\n"
            f"👤 @{message.from_user.username or 'Ad yoxdur'}\n"
            f"{message.text}\n\n"
            f"🆔 Chat ID: {message.chat.id}"
        )
        bot.send_message(GROUP_CHAT_ID, forward_text)

# Botu işə salırıq
bot.polling()
