import telebot
from telebot import types
import time
import json
from get_weather import get_data

API_BOT = open('api_bot', 'r').read()
bot = telebot.TeleBot(API_BOT)

#commit for check

@bot.message_handler(commands=['start', '/help'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Выбрать город')
    button2 = types.KeyboardButton('Узнать погоду')
    button3 = types.KeyboardButton('/start')
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id , "Привет! Я бот, который поможет тебе узнать текущую температуру.", reply_markup=markup)
    time.sleep(1)
    bot.send_message(message.chat.id, "Выбери дальнешее действие:" )

def save_city(message):
    city = message.text
    
    for char in str(message.text):
        if char.isdigit():
            bot.send_message(message.chat.id, f"Город не должен содержать цифр")
            return
        
    with open('citys.json', 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
                
    data[str(message.chat.id)] = city
        
    with open('citys.json', 'w') as file:
        json.dump(data, file, indent=4)
        
    bot.send_message(message.chat.id, f"Город {city} сохранен.")

@bot.message_handler(func=lambda message: message.text == "Выбрать город")
def choose_city(message):
    bot.send_message(message.chat.id, "Введите название города:")
    bot.register_next_step_handler(message, save_city)

@bot.message_handler(func=lambda message: message.text == "Узнать погоду")
def main(message):
    with open('citys.json', 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}

    chat_id = str(message.chat.id)
    if chat_id in data:
        city = str(data[chat_id])
        weather_info = get_data(city)
        bot.send_message(message.chat.id, weather_info)
        
bot.infinity_polling()