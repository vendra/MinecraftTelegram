# Minecraft Telegram Bot

A telegram bot that allows a private Minecraft server management. It was initially developed to send the dynamic IP of the server each day to the telegram group where the bot was added.

#### Command List
- **/start**  start the bot and display available commands
- **/status** Display the server status: Online/Offline, Public IP, Player Count / Max Player
- **/shutdown <timeout>** Shutdown the server, timeout in seconds. Default is 30s (0 < timeout <= 300s)
- **/restart <timeout>** Restart the server, start if not running. Timeout in seconds. Default 30s (0 < timeout <= 300s)
- **/stats <time>** Check CPU usage over the specified time window. Default is 3s (0 < timeout <= 60s)
- **/info** Display some info about the author and link to this github repository


## Features 
- Check **Server Status**, public IP and number players connected
- Server **Shutdown** + **Restart** with timer and telegram ID privilege check
- Server **Statistics** to check memory usage and CPU load over window time


##  Install
- **Clone** or download the repository
- Create a telegram bot as specified [HERE](https://core.telegram.org/bots#6-botfather) and get the token
- Edit the **config.ini** file:
    - Insert your bot's token
    - Fill the admin list with telegram IDs (no need for '@') that will have permission to restart and shutdown commands
    - Edit the path to your server .jar
    - Edit the Xmx and Xms parameters to set the starting and max server memory
- Now you can **start** the bot using:
```python MinecraftServerBot.py```
**Note**: it will also automatically start the server
