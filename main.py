import telebot 
from config import token
import random

from logic import *

bot = telebot.TeleBot(token) 
#Команда для создания покемона
@bot.message_handler(commands=['create'])
def start(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1,3)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 2:
            pokemon = Wizard(message.from_user.username)
        elif chance == 3:
            pokemon = Fighter(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")
#Команда для удаления покемона
@bot.message_handler(commands=['delete'])
def delete_pokemon(message):
    username = message.from_user.username

    if username in Pokemon.pokemons:
        del Pokemon.pokemons[username]
        bot.send_message(message.chat.id, "🗑️ Твой покемон удалён!")
    else:
        bot.send_message(message.chat.id, "❌ У тебя нет покемона!")

#Комманда для атаки покемонов
@bot.message_handler(commands=["attack"])
def attack(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщения того, кого хочешь атаковать")
#Команда для кормления покемона
@bot.message_handler(commands=['feed'])
def feed_pok(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        response = pok.feed()
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "У вас нет покемона!")
#Команда дял информации о покемоне
@bot.message_handler(commands=['info'])
def info(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        respons = pok.info()
        bot.send_message(message.chat.id, respons)
    else:
        bot.send_message(message.chat.id, "У вас нет покемона")
bot.infinity_polling(none_stop=True)

