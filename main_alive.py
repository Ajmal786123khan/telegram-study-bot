import telebot
import threading
from keep_alive import keep_alive

bot1 = telebot.TeleBot("8553289877:AAGIUHX2PEu-xCjlw3EQOD8p1E206DVHNYc")
bot2 = telebot.TeleBot("8437748698:AAErdBGclNfK9C05CBuyu6uPdA1ohXZXggk")

keep_alive()

@bot1.message_handler(commands=['start'])
def start1(message):
    bot1.reply_to(message, "Bot 1 working!")

@bot2.message_handler(commands=['start'])
def start2(message):
    bot2.reply_to(message, "Bot 2 working!")

def run_bot1():
    bot1.polling()

def run_bot2():
    bot2.polling()

threading.Thread(target=run_bot1).start()
threading.Thread(target=run_bot2).start()
