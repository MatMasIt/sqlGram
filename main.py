import configparser
import json

import colorama
import pymysql.cursors
import telebot
from tabulate import tabulate

import init

colorama.init()

config = configparser.ConfigParser()

config.read("conf.ini")

bot = telebot.TeleBot(config["DATA"]["token"].strip())

connection = pymysql.connect(host=config["DB"]["host"],
                             port=int(config["DB"]["port"]),
                             user=config["DB"]["user"],
                             password=config["DB"]["password"],
                             database=config["DB"]["database"],
                             cursorclass=pymysql.cursors.DictCursor)

fInit = init.init(config)
if fInit:
    print("Initialization token: " + colorama.Fore.GREEN + fInit + colorama.Style.RESET_ALL)


@bot.message_handler(commands=['start'])
def start(message):
    if fInit:
        bot.reply_to(message, "Send me the initialization token")
    else:
        bot.reply_to(message, "Welcome to this bot, you are authenticated")


@bot.message_handler(func=lambda message: fInit)
def echo_all(message):
    global fInit
    if message.text.strip() != config["DATA"]["masterToken"]:
        bot.reply_to(message, "Wrong Token")
    else:
        init.setInited(config, message.chat)
        fInit = False
        bot.reply_to(message, "The bot has been initialized. You may now send queries")


@bot.message_handler(func=lambda message: True)
def queries(message):
    global connection
    if str(message.chat.id) not in config["DATA"]["allowedids"].split(","):
        bot.send_message(message.chat.id, "You are not authorized")
        return False
    bot.send_message(message.chat.id, "Working ...")
    mode = "TABLE"
    if message.text.startswith("JSON "):
        mode = "JSON"
        message.text = message.text[5:]
    elif message.text.startswith("CSV "):
        mode = "CSV"
        message.text = message.text[4:]

    try:
        if message.text.strip().upper() == "COMMIT":
            connection.commit()
            bot.send_message(message.chat.id, "Committed")
        elif message.text.strip().upper() == "BEGIN TRANSACTION":
            bot.send_message(message.chat.id,
                             "The BOT works always in a transaction until you COMMIT, then it starts a new one")
        elif message.text.strip().upper() == "ROLLBACK":
            connection.rollback()
            bot.send_message(message.chat.id, "Rollbacked")
        elif message.text.strip().upper() == "CLOSE":
            connection.close()
            bot.send_message(message.chat.id, "Closed")
        elif message.text.strip().upper() == "OPEN":
            connection = pymysql.connect(host=config["DB"]["host"],
                                         port=int(config["DB"]["port"]),
                                         user=config["DB"]["user"],
                                         password=config["DB"]["password"],
                                         database=config["DB"]["database"],
                                         cursorclass=pymysql.cursors.DictCursor)
            bot.send_message(message.chat.id, "Opened")
        else:
            with connection.cursor() as cursor:
                sql = message.text
                cursor.execute(sql)
                res = cursor.fetchall()
                if len(res):
                    if mode == "JSON":
                        info = json.dumps(res)
                    elif mode == "CSV":
                        info = ",".join(res[0].keys()) + "\n"
                        for row in res:
                            info += ",".join(list(row.values())) + "\n"
                    else:
                        resultsTable = []
                        for row in res:
                            resultsTable.append(list(row.values()))
                        info = tabulate(resultsTable, headers=res[0].keys())
                    info = "```\n"+info+"\n```"
                    if len(info) > 4096:
                        r = open("results.txt", "w+")
                        r.write(info)
                        r.close()
                        with open("results.txt", "rb") as file:
                            bot.send_document(message.chat.id, file)
                    else:
                        bot.send_message(message.chat.id, info)
    except Exception as e:
        bot.reply_to(message, str(e))
        print(e)
    bot.send_message(message.chat.id, "Done ...")


@bot.edited_message_handler(func=lambda message: True)
def handle(message):
    queries(message)


bot.polling()
