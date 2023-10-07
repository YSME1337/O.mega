import telebot
import sqlite3
import re

conn = sqlite3.connect('database1.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   message TEXT)''')
conn.commit()

bot = telebot.TeleBot("6696600921:AAE01WUudUdsrxWk8MAsWuyeCT0hM_gdN0M")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который использует данные из базы данных и отвечает на основе AI.")


def handle_message(message):
    user_input = message.text
    street_match = re.search(r'улица\s+(\S+)', user_input)
    house_number_match = re.search(r'дом\s+(\S+)', user_input)
    street = street_match.group(1) if street_match else None
    house_number = house_number_match.group(1) if house_number_match else None
    cursor.execute("INSERT INTO messages (user_id, message, street, house_number) VALUES (1, 1, 1, ?)",
                   (message.from_user.id, user_input, street, house_number))
    conn.commit()
    cursor.execute("INSERT INTO messages (user_id, message) VALUES (?, ?)", (message.from_user.id, user_input))
    conn.commit()
    # Use data from the database and AI to formulate a response
    # Here you can use your AI model to generate a response based on the data from the database
    bot.reply_to(message, generated_response)


@bot.message_handler(func=lambda message: True)
def respond_to_user_message(message):
    handle_message(message)


bot.polling()
ч