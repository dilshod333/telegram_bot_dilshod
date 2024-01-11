


import telebot
from datetime import datetime
import random
from telebot import types
import requests

bot = telebot.TeleBot("6602460824:AAFi7PBLivM0RMIEpAMTCWIJ5oXN-p-_OrI")



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Sizga qanday yordam berolaman {message.from_user.first_name}")






def get_exchange_rates():
    url = "https://v6.exchangerate-api.com/v6/9bfef0c3f2456d2a6142c5df/latest/USD"
    response = requests.get(url)
    answer = response.json()
    return answer['conversion_rates']

def show_exchange_rate(message):
    exchange_rates = get_exchange_rates()
    message_text = f"Salom {message.from_user.first_name}\n 1 Dollor kursi \n"

    for currency, rate in exchange_rates.items():
        if currency == 'UZS':
            message_text += f"{currency}: {rate}\n"

    bot.send_message(message.chat.id, message_text)

def get_weather(message):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    city = "Tashkent"

    params = {
        'q': city,
        'appid': '04913d3529a596d1a9b6e6717ef409dc',
        'units': 'metric'  # Use 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        print(data)

        if response.status_code == 200:
            w = f""" Weather in {city}:\n\nTemperature: {data['main']['temp']}°C/\n\nDescription: {data['weather'][0]['description']}\n\nWind Speed: {data['wind']['speed']} m/s """

            bot.send_message(message.chat.id, w)
        else:
            bot.send_message(message.chat.id, f"Error: : {response.status_code}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['start'])
def button(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn = types.KeyboardButton("Time")
    btn2 = types.KeyboardButton("Game")
    btn3 = types.KeyboardButton("Dollar kursi")
    btn4 = types.KeyboardButton("Ob-havo")
    btn5 = types.KeyboardButton("Bekorchi ")
    markup.add(btn, btn2, btn3, btn4,btn5)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)
    print(message.text)

@bot.message_handler(func=lambda message: True)
def handle(message):
    if message.text == 'Time':
        now = datetime.now()
        data_time = now.strftime("%d/%m/%y\n\nTime %H:%M:%S")
        bot.reply_to(message, data_time)
    elif message.text == 'Game':
        user_question = [
            {'question': "What is the capital of France", 'answer': "Paris"},
            {'question': "What is the best car in the world", 'answer': "BMW"},
            {'question': "Do you like yourself", 'answer': "yes"}
        ]

        r = random.choice(user_question)
        bot.send_message(message.chat.id, f'Question is {r["question"]}')
        bot.register_next_step_handler(message, lambda msg: answer(msg, r))

    elif message.text == 'Dollar kursi':
        show_exchange_rate(message)

    elif message.text == 'Ob-havo':
        get_weather(message)

    elif message.text == 'Bekorchi':
        bot.send_message(message.chat.id, f'{message.from_user.first_name} it is in proccess... ')


def answer(message, current_question):
    print(message.text)
    if message.text.lower() == current_question['answer'].lower():
        bot.send_message(message.chat.id, 'You are right!')

    else:
        bot.send_message(message.chat.id, 'You are not correct!')


@bot.message_handler(commands=['userinfo'])
def userinfo(message):
    bot.send_message(message.chat.id, "Enter your name ")


#
@bot.message_handler(func=lambda message: True)
def get_info(message):
    bot.reply_to(message, "Your information saved ")

    with open("bot_f.txt", 'w') as file:
        file.write(message.text)

bot.infinity_polling()
