import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8318840240:AAGRrn3gzcdb5doSNf30v81YWmLlPn8_6S8'
bot = telebot.TeleBot(TOKEN)

# Men� d�ym?l?ri
main_menu = InlineKeyboardMarkup(row_width=1)
main_menu.add(
    InlineKeyboardButton("Haqqimizda", callback_data="about"),
    InlineKeyboardButton("?laq?", callback_data="contact"),
    InlineKeyboardButton("Veb sayt", callback_data="website"),
    InlineKeyboardButton("test1", callback_data="test1"),
    InlineKeyboardButton("test2", callback_data="test2")
)

# Baslangic mesaji
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Salam! Asagidaki m�vzulardan birini se�in:",
        reply_markup=main_menu
    )

# Callback funksiyasi � d�ym? klikl?n?nd? cavab verilir
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "about":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "IT il? bagli b�t�n xidm?tl?ri g�st?ririk")
    elif call.data == "contact":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "+994511111111")
    elif call.data == "website":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "Veb saytlar 300 azn")
    elif call.data == "test1":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "test1")
    elif call.data == "test2":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "test2")

bot.polling()