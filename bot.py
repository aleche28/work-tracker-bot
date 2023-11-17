import os
from dotenv import load_dotenv
import telebot
from github import get_github_repo_stats
from youtrack import get_time_spent_per_user
import random

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
STICKER_SET_NAME = os.getenv('STICKER_SET_NAME')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def print_intro(message):
    intro_msg = 'This is a bot to track the time spent working by each member of group 15 of SoftEng II'
    bot.reply_to(message, intro_msg)

@bot.message_handler(commands=['hello'])
def print_hello(message):
    bot.reply_to(message, 'Hello world!')

@bot.message_handler(commands=['menu'])
def print_menu(message):
    menu = 'Available commands: idk just open the command menu...'
    bot.reply_to(message, menu)

@bot.message_handler(commands=['spent'])
def print_user_spent_time(message):
    ranking = get_time_spent_per_user()
    bot.reply_to(message, ranking, parse_mode="markdownv2")

@bot.message_handler(commands=['commits'])
def print_commits(message):
    commits = get_github_repo_stats()
    bot.reply_to(message, commits, parse_mode="markdownv2")

@bot.message_handler(commands=['sticker'])
def send_sticker(message):
    sticker_set = bot.get_sticker_set(STICKER_SET_NAME)
    sticker = random.choice([sticker_set.stickers[0], sticker_set.stickers[39]])
    bot.send_sticker(message.chat.id, sticker.file_id, message.message_id)

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "pong")

# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     bot.reply_to(message, "Please write a command that I can understand bro")

bot.infinity_polling()
