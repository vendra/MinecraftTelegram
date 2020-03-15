#!/usr/bin/env python

import configparser

import psutil
import subprocess
import telegram
import time
import urllib.request

from telegram.ext import Updater, CommandHandler
import server_utils

class MinecraftServerBot:
    def __init__(self, ip, token, process, config):
        self.ip = ip
        self.process = process
        self.config = config
        self.adminIDs = self.config['SETTINGS']['adminIDs'].split(',')
        print("Admin IDs: " + str(self.adminIDs))
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
            if self.process.poll() is None:
                seconds = 30
                if len(context.args) == 1:
                    try:
                        seconds = int(context.args[0])
                        if seconds < 0 or seconds > 300:
                            context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                                     text="Invalid time, must be between 0 and 300 seconds.\n"
                                                          "Using default = 30 seconds!")
                    except Exception as e:
                        print("Exception " + str(e))

                context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                         text="Shutting down the server in " + str(seconds) + " seconds!!")
                self.process.stdin.write("/say Shutting down the server in " + str(seconds) + " seconds!!\r\n")
                self.process.stdin.flush()
                time.sleep(seconds)

                context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                         text="Shutting down the server NOW!!")
                self.process.stdin.write("/say Shutting down the server NOW!!\r\n")
                self.process.stdin.flush()
                time.sleep(3)

                # Terminate
                self.process.terminate()

                context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                         text="Server shutdown!")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                         text="Server already Offline!!")


    def restart(self, update, context):
        if update.effective_user['username'] in self.adminIDs:
            # Terminate First
            if self.process.poll() is None:
                seconds = 30
                if len(context.args) == 1:
                    try:
                        seconds = int(context.args[0])
                        if seconds < 0 or seconds > 300:
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     parse_mode=telegram.ParseMode.HTML,
                                                     text="Invalid time, must be between 0 and 300 seconds.\n"
                                                          "Using default = 30 seconds!")
                    except Exception as e:
                        print("Exception " + str(e))

                context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                         text="Restarting the server in " + str(seconds) + " seconds!!")
                self.process.stdin.write("/say Restarting the server in " + str(seconds) + " seconds!!\r\n")
                self.process.stdin.flush()
                time.sleep(seconds)

                context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                         text="Restarting the server NOW!!")
                self.process.stdin.write("/say Restarting the server NOW!!\r\n")
                self.process.stdin.flush()
                time.sleep(3)

                # Terminate
                self.process.terminate()


            # Restart the Server
            self.process = subprocess.Popen("java -Xmx" + self.config['SERVER']['Xmx'] + "M -Xms" + self.config['SERVER']['Xms']
                                            + "M -jar " + self.config['SERVER']['serverJarPath'] + " nogui",
                                            bufsize=1, universal_newlines=True, stdin=subprocess.PIPE)
            time.sleep(10)
            print("Process PID: " + str(self.process.pid))
            if self.process.poll() is None:
                context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                     text="Server Online!")

    def status(self, update, context):

        player_count = 0
        player_max = 0

        status = 'Offline'
        if self.process.poll() is None:
            status = 'Online'
            server_descriptor = server_utils.get_server_descriptor()
            if server_descriptor is not None:
                player_count = server_descriptor[1]
                player_max = server_descriptor[2]

        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text="<b>Status</b> : " + status + "\n" +
                                      "<b>Address</b>: " + self.ip +
                                      "<b>Players</b>: " + str(player_count) + "/" + str(player_max))

    def info(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                 text='<b>Author</b>: <a href="https://www.linkedin.com/in/federico-vendramin">Federico Vendramin</a>\n'
                                      '<b>Email</b>: Federico.Vendramin@gmail.com\n'
                                      '<b>Source</b>: <a href="https://github.com/vendra/MinecraftTelegram">Github Repository</a>')
                                      #'<a href="https://www.linkedin.com/in/federico-vendramin">LinkedIn Profile</a>')
                                      #"<b>Git</b>: https://github.com/vendra/MinecraftTelegram\n"
                                      #"<b>LinkedIn</b>: https://www.linkedin.com/in/federico-vendramin")

    def stats(self, update, context):
        seconds = 3
        if len(context.args) == 1:
            try:
                seconds = int(context.args[0])
                if seconds < 1 or seconds > 60:
                    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                             text="Invalid time, must be between 1 and 60 seconds.\n"
                                                  "Using default = 3 seconds!")
            except Exception as e:
                print("Exception " + str(e))
                context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=telegram.ParseMode.HTML,
                                         text="Invalid time, must be between 1 and 60 seconds.\n"
                                              "Using default = 3 seconds!")

        cpu_load = psutil.cpu_percent(interval=seconds)
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
    time.sleep(10)
    print("Process PID: " + str(process.pid))

    bot = MinecraftServerBot(external_ip, config['SETTINGS']['TelegramToken'], process, config)
    bot.start_polling()


if __name__ == "__main__":
    main()