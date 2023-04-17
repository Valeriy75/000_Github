import telebot
from config import config
import requests


bot = telebot.TeleBot(config['token'])

GREETING_REPLY = (
    'Приветствуйю! Я бот для экзамена по дисциплине "Основы Python"\n'
    'Я представляю из себя калькулятор для расчета валюты на основе '
    'курса ЦБ РФ.\nВам предстоит дополнить мой функционал.'
)


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    get_currency_btn = telebot.types.InlineKeyboardButton(
        'Получить курс валют',
        callback_data='get_currency_callback'
    )
    markup.add(get_currency_btn)
    bot.send_message(
        message.chat.id,
        GREETING_REPLY,
        reply_markup=markup
    )


@bot.message_handler(commands=['help'])
def help(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    get_currency_btn = telebot.types.InlineKeyboardButton(
        'Получить курс валют',
        callback_data='get_currency_callback'
    )
    markup.add(get_currency_btn)
    bot.send_message(
        message.chat.id,
        GREETING_REPLY + (
            '\n\nУ меня есть следующие команды'
        ),
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == 'get_currency_callback')
@bot.message_handler(commands=['get_currency'])
def choose_currency(call):
    if type(call) == telebot.types.Message:
        chat_id = call.chat.id
    else:
        chat_id = call.message.chat.id
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    usd_btn = telebot.types.InlineKeyboardButton('USD', callback_data='get_usd_value')
    eur_btn = telebot.types.InlineKeyboardButton('EUR', callback_data='get_eur_value')
    amd_btn = telebot.types.InlineKeyboardButton('AMD', callback_data='get_amd_value')
    markup.add(usd_btn, eur_btn, amd_btn)
    bot.send_message(
        chat_id,
        (
            'Выберите валюту для получения курса'
        ),
        reply_markup=markup
    )


@bot.callback_query_handler(
    func=lambda call: call.data in ['get_usd_value', 'get_eur_value', 'get_amd_value']
)
def choose_currency_level(call):
    if call.data == 'get_usd_value':
        currency = 'USD'
        json_answer = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        value = json_answer['Valute']['USD']['Value']
    elif call.data == 'get_eur_value':
        currency = 'EUR'
        json_answer = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        value = json_answer['Valute']['EUR']['Value']
    else:
        currency = 'AMD'
        json_answer = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        value = json_answer['Valute']['AMD']['Value']

    bot.send_message(
        call.message.chat.id,
        (
            f'Вы выюрали валюту - {currency}\n'
            f'Текущий курс к рублю - {value}'
        )
    )


bot.polling(non_stop=True, interval=0)
