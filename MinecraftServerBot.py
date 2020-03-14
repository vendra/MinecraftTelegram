#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler
import configparser, telegram
import urllib.request
import time, subprocess

class MinecraftServerBot:
    def __init__(self, ip, token, process, config):
        self.ip = ip
        self.process = process
        self.config = config
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
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="Hello! Available commands: \n" +
                                 "\\start\n\\shutdown\n\\restart\n\\status\n\\info")

    # TODO Implement? Security access?
    # Use default time? accept as parameter?
    def shutdown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="Shutting down the server!")
        # Terminate
        if self.process.poll() == None:
            self.process.terminate()

        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="Server shutdown!")

    # TODO Implement? Security access?
    def restart(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="Restarting the server!")
        # Terminate First
        if self.process.poll() == None:
            self.process.terminate()
            time.sleep(1)

        # Restart the Server
        self.process = subprocess.Popen(
            "java -Xmx" + self.config['SERVER']['Xmx'] + "M -Xms" + self.config['SERVER']['Xms'] + "M -jar " +
            self.config['SERVER']['serverJarPath'] + " nogui")
        time.sleep(3)
        print("Process PID: " + str(self.process.pid))
        if self.process.poll() == None:
            context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="Server Online!")

    # TODO Add Connected Players?
    def status(self, update, context):
        status = 'Offline'
        if self.process.poll() == None:
            status = 'Online'

        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="<b>Status</b> : "+status+"\n" +
                                      "<b>Address</b>: " + self.ip +
                                      "<b>Players</b>: X/X")

    def info(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="<b>Author</b>: Federico Vendramin\n"
                                       "<b>Email</b>: federico.vendramin@gmail.com\n"
                                       "<b>Git</b>: https://github.com/vendra/MinecraftTelegram")

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()

    # Get the Server Address
    external_ip = urllib.request.urlopen(config['SETTINGS']['ServiceProvider']).read().decode('utf8')
    print("Machine Address: " + external_ip)

    # Start the Server
    process = subprocess.Popen("java -Xmx" + config['SERVER']['Xmx'] + "M -Xms" + config['SERVER']['Xms'] + "M -jar " +
                     config['SERVER']['serverJarPath'] + " nogui")
    time.sleep(3)
    print("Process PID: " + str(process.pid))

    bot = MinecraftServerBot(external_ip, config['SETTINGS']['TelegramToken'], process, config)
    bot.start_polling()


if __name__ == "__main__":
    main()