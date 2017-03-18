from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import logging
from subprocess import call, Popen, PIPE
import uuid
from os import remove
from threading import Timer
import time
import asyncio
import threading
import re

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token='352175520:AAHhhY5qbFyLtPYTbbzHi7U1v1SlAmr9iWk')
dispatcher = updater.dispatcher

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="""Ну давай сучара напиши свои слова""")

def del_file(file, name):
    file.close()
    remove(name)

@run_async
def receive_text(bot, update):
    """ Method that runs forever """
    user = update.message.from_user
    username = user.first_name
    username = re.sub(r'\W+', '', username)
    randomname = username + str(time.time())
    text_file = open(randomname+'.txt', "w")
    message = str(update.message.text)
    if len(message) > 100:
        message = """Много бу<кв, штук {}, мне влом столько читать""".format(len(message))
    
    text_file.write(message)
    text_file.close()
    logging.info("""{} sent {}""".format(user.first_name, message))
    call("""balcon.exe -f {}.txt -w {}.wav -n "Digalo Russian Nicolai""".format(randomname, randomname), shell=True)
    #call("""Govorilka_cp.exe -E "Digalo Russian Nicolai" -q -f {}.txt -TO {}.wav""".format(randomname, randomname), shell=True)
    audio_file = open(randomname+'.wav', "rb")
    
    remove(randomname+'.txt')
    bot.sendVoice(update.message.chat_id, audio_file)
    del_file(audio_file, randomname+'.wav')
    #Timer(300, del_file, (audio_file, randomname+'.wav',)).start()

text_handler = MessageHandler(Filters.text, receive_text)
dispatcher.add_handler(text_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
