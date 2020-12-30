# main.py
import os
import discord
from dotenv import load_dotenv
from datetime import datetime

# setup actual bot
intents = discord.Intents.all()
bot = discord.Client(intents=intents)

# globals and env
# you will need to set this in your .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# import funcs
import cfg
import handlers

# core
class BotClient(discord.Client):
        
    # bot is ready
    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        await bot.change_presence(activity=discord.Game(name='with catgirls'))

        # setup and load config
        if(os.path.exists('config/bot/settings')):
            print('Config file exists, reading')
            cfg.config.read('config/bot/settings')
        else:
            print('Config does not exist, creating')
            cfg.config['SERVER'] = {
                'filterRole' : '',
                'filter' : [],
                'prefix' : '?',
                'loggingEnabled' : 'yes'
            }
            os.mkdir('config')
            os.mkdir('config/bot')
            with open('config/bot/settings', 'w') as file:
                cfg.config.write(file)


        # log folder
        if(os.path.exists('logs')):
            print('Logs folder already exists')
        else:
            print('Logs folder does not yet exist, creating now.')
            os.mkdir('logs')
            os.mkdir('logs/startup')
            os.mkdir('logs/messages')

        # log startup
        f = open(f'logs/startup/startup.log', 'a')
        f.write(f'{str(datetime.now())} {bot.user} is now online in {len(bot.guilds)} guilds!\n')
        f.close

    # message send event
    @bot.event
    async def on_message(message):
        # get guild
        try:
            guild = message.channel.guild
        except:
            # not guild
            return

        # log message
        await handlers.logMessage(message)

        # if it is the bot, return
        if message.author == bot.user:
            return

        if(message.content.startswith(cfg.config['SERVER']['prefix'])):
            await handlers.checkCommands(guild, message)
        else:
            await handlers.checkMessage(guild, message)

bot.run(TOKEN)