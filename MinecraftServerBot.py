#!/usr/bin/env python

import configparser
import psutil
import subprocess
import telegram
import time
import urllib.request

from telegram.ext import Updater, CommandHandler


class MinecraftServerBot:
    def __init__(self, ip, token, process, config):
        self.ip = ip
        self.process = process
        self.config = config
        self.adminIDs = self.config['SETTINGS']['adminIDs'].split(',')
        print("Admin IDs: " + self.adminIDs)
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

        self.stats_handler = CommandHandler('stats', self.stats)
        self.dispatcher.add_handler(self.stats_handler)

    def start_polling(self):
        self.updater.start_polling()

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="Hello! Available commands: \n" +
                                 "/start\n/shutdown\n/restart\n/status\n/info\n/stats")

    # Use default time? accept as parameter?
    def shutdown(self, update, context):
        if update.effective_user['username'] in self.adminIDs:
            self.process.stdin.write("/say Shutting down the server NOW!!\r\n")
            self.process.stdin.flush()
            time.sleep(3)
            context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                     text="Shutting down the server!")
            # Terminate
            if self.process.poll() is None:
                self.process.terminate()

            context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                     text="Server shutdown!")

    def restart(self, update, context):
        if update.effective_user['username'] in self.adminIDs:
            context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                     text="Restarting the server!")
            # Terminate First
            if self.process.poll() is None:
                self.process.stdin.write("/say Restarting the server NOW!!\r\n")
                self.process.stdin.flush()
                time.sleep(3)
                self.process.terminate()
                time.sleep(1)

            # Restart the Server
            self.process = subprocess.Popen("java -Xmx" + self.config['SERVER']['Xmx'] + "M -Xms" + self.config['SERVER']['Xms']
                                            + "M -jar " + self.config['SERVER']['serverJarPath'] + " nogui",
                                            bufsize=1, universal_newlines=True, stdin=subprocess.PIPE)
            time.sleep(3)
            print("Process PID: " + str(self.process.pid))
            if self.process.poll() is None:
                context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                     text="Server Online!")

    # TODO Add Connected Players?
    def status(self, update, context):
        status = 'Offline'
        if self.process.poll() is None:
            status = 'Online'

        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="<b>Status</b> : "+status+"\n" +
                                      "<b>Address</b>: " + self.ip +
                                      "<b>Players</b>: X/X")

    def info(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text='<b>Author</b>: <a href="https://www.linkedin.com/in/federico-vendramin">Federico Vendramin</a>\n'
                                      '<b>Email</b>: Federico.Vendramin@gmail.com\n'
                                      '<b>Source</b>: <a href="https://github.com/vendra/MinecraftTelegram">Github Repository</a>')
                                      #'<a href="https://www.linkedin.com/in/federico-vendramin">LinkedIn Profile</a>')
                                      #"<b>Git</b>: https://github.com/vendra/MinecraftTelegram\n"
                                      #"<b>LinkedIn</b>: https://www.linkedin.com/in/federico-vendramin")

    def stats(self, update, context):
        cpu_load = psutil.cpu_percent(interval=2)
        mem = psutil.virtual_memory()
        mem_load = 100 * mem.used / mem.total

        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="<b>CPU Load</b>: " + str(cpu_load) + "%\n"
                                 "<b>Memory</b>: " + str(int(mem.used / 1048576)) + "MB / " + str(int(mem.total / 1048576))
                                 + "MB\n<b>Memory Load</b>: " + str(round(mem_load, 2)) + "%")


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()

    # Get the Server Address
    external_ip = urllib.request.urlopen(config['SETTINGS']['ServiceProvider']).read().decode('utf8')
    print("Machine Address: " + external_ip)

    # Start the Server
    process = subprocess.Popen("java -Xmx" + config['SERVER']['Xmx'] + "M -Xms" + config['SERVER']['Xms'] + "M -jar " +
                               config['SERVER']['serverJarPath'] + " nogui", bufsize=1, universal_newlines=True,
                               stdin=subprocess.PIPE)
    time.sleep(3)
    print("Process PID: " + str(process.pid))

    bot = MinecraftServerBot(external_ip, config['SETTINGS']['TelegramToken'], process, config)
    bot.start_polling()


if __name__ == "__main__":
    main()