#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler
import configparser
import urllib.request

class MinecraftServerBot:
    def __init__(self, ip, token):
        self.ip = ip
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(self.start_handler)

        self.shutdown_handler = CommandHandler('shutdown', self.shutdown)
        self.dispatcher.add_handler(self.shutdown_handler)

        self.restart_handler = CommandHandler('restart', self.restart)
        self.dispatcher.add_handler(self.restart_handler)

        self.status_handler = CommandHandler('status', self.status)
        self.dispatcher.add_handler(self.status_handler)

        self.info_handler = CommandHandler('info', self.info)
        self.dispatcher.add_handler(self.info_handler)


    def start_polling(self):
        self.updater.start_polling()

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML, text="bot test")

    # TODO Implement? Security access?
    # Use default time? accept as parameter?
    def shutdown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="Server Shutdown not implemented yet!")

    # TODO Implement? Security access?
    def restart(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="Server Restart not implemented yet!")

    # TODO Check Server Online/Offline
    # TODO Add Connected Players?
    def status(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="<b>Status</b> : Online/Offline\n" +
                                      "<b>Address</b>: " + self.ip +
                                      "<b>Players</b>: X")


    def info(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="<b>Author</b>: Federico Vendramin\n"
                                       "<b>Email</b>: federico.vendramin@gmail.com\n"
                                       "<b>Git</b>: https://github.com/vendra/MinecraftTelegram")

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()

    external_ip = urllib.request.urlopen(config['SETTINGS']['ServiceProvider']).read().decode('utf8')
    print("Machine Address: " + external_ip)

    bot = MinecraftServerBot(external_ip, config['SETTINGS']['TelegramToken'])
    bot.start_polling()


if __name__ == "__main__":
    main()