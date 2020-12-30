import discord
from datetime import datetime
from dotenv import load_dotenv

import sys, traceback, os
import cfg

load_dotenv()

# cog list
cogs = [
    'cogs.basic',
    'cogs.filter',
    'cogs.mod',
    'cogs.config'
]

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    print(f'Loading {len(cogs)} cogs!')

    for extension in cogs:
        cfg.bot.load_extension(extension)
    
    print('') # newline

@cfg.bot.event
async def on_ready():
    print(f'{cfg.bot.user} has connected to Discord!')
    await cfg.bot.change_presence(activity=discord.Game(name='with catgirls'))

    # setup and load config
    if(os.path.exists('config/bot/settings.ini')):
        print('Config file exists, reading')
        cfg.config.read('config/bot/settings.ini')
    else:
        print('Config does not exist, creating')
        cfg.config['SERVER'] = {
            'filterRole' : '',
            'filter' : [],
            'prefix' : '?',
            'loggingEnabled' : 'yes',
            'modrole' : ''
        }
        os.mkdir('config')
        os.mkdir('config/bot')
        with open('config/bot/settings.ini', 'w') as file:
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
    f.write(f'{str(datetime.now())} {cfg.bot.user} is now online in {len(cfg.bot.guilds)} guilds!\n')
    f.close

    print(f'Successfully logged in and booted!')
    print('') # newline


cfg.bot.run(os.getenv('DISCORD_TOKEN'), bot=True, reconnect=True)