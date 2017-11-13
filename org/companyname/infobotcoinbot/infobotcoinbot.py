import telebot
import os
import requests
from flask import Flask, request

# set up config variables en your heroku environment
# your bot TOKEN
token = os.environ.get('TOKEN')
# your heroku app URL and add path "bot" for active update
appURL = os.environ.get('APPURL') + '/bot'
# end of read config variables

bot = telebot.TeleBot(token)

server = Flask(__name__)

# on the start command to user would send a userkeyboard
@bot.message_handler(commands=['start'])
def start(message):
    # create userkeyboard, resize = true, autohide=true
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("/Bitcoin", "/Ethereum")
    user_markup.row("/BitConnect", "/BitcoinCash")
    user_markup.row("/settings")

    # send a message to a user with new keyboard
    bot.send_message(message.from_user.id, 'Hello, ' + message.from_user.first_name
                     + '. I am your Crypto Coins Info Bot! Use a keyboard for receive info about a price of a crypto coin.',
                     reply_markup=user_markup)

# for reply for user with its own message
# @bot.message_handler(func=lambda message: True, content_types=['text'])
#def echo_message(message):
#    bot.reply_to(message, message.text)
# end

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=appURL)
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)