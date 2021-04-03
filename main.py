import telebot
import pickle
import random

# 1743116356:AAFUb9wRDF5xXHBHWCKITUeAX7RySsrbeb8
bot = telebot.TeleBot('1743116356:AAFUb9wRDF5xXHBHWCKITUeAX7RySsrbeb8', parse_mode=None)
greet = ['Ну ты лютый как Тайкус', 'А малыш Джимми', 'Может лучше на шашлычки с Империем?', 'Время собирать души',
         'Смотрите, кто воскрес']


class User:
    def __init__(self):
        self.today = {0: 0}
        self.today_count = {0: {0: 0}}

    def plus_call(self, plus, user_id):
        self.today_count[user_id][self.today[user_id]] += plus
        pickle.dump(self.today_count, open('save.txt', 'wb'))

    def minus_call(self, minus=0, user_id=0):
        self.today_count[user_id][self.today[user_id]] -= minus
        pickle.dump(self.today_count, open('save.txt', 'wb'))

    def new_day(self, user_id):
        self.today[user_id] += 1
        self.today_count[user_id][self.today[user_id]] = 0
        pickle.dump(self.today_count, open('save.txt', 'wb'))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Пора в качалку, брат")
    general.today_count[message.from_user.id] = {0: 0}
    general.today[message.from_user.id] = 0
    try:
        load()
    except EOFError:
        pass


@bot.message_handler(commands=['new_day'])
def new_day(message):
    general.new_day(message.from_user.id)
    bot.send_message(message.from_user.id, random.choice(greet))


def load():
    general.today_count = pickle.load(open('save.txt', 'rb'))


@bot.message_handler(func=lambda m: True)
def call(message):
    test = message.text
    try:
        count_call = int(test[1:])
    except ValueError:
        bot.send_message(message.from_user.id, 'Ошибка: Формат ввода +/- число')
        count_call = 0

    act = str(test[0])
    if act == '+':
        general.plus_call(count_call, message.from_user.id)
        bot.send_message(message.from_user.id,
                         general.today_count[message.from_user.id][general.today[message.from_user.id]])
    elif act == '-':
        general.minus_call(count_call, message.from_user.id)
        bot.send_message(message.from_user.id,
                         general.today_count[message.from_user.id][general.today[message.from_user.id]])
    else:
        bot.send_message(message.from_user.id, 'Ошибка: Формат ввода +/- число')


general = User()
bot.polling()
