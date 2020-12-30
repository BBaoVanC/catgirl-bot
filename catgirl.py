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

async def connected():

    # log folder
    if(os.path.exists('logs')):
        print('Logs folder already exists')
    else:
        print('Logs folder does not yet exist, creating now.')
        os.mkdir('logs')
        os.mkdir('logs/startup')
        os.mkdir('logs/guilds')


    # setup and load config for each guild
    for guild in cfg.bot.guilds:
        if guild.name == None:
            return

        if os.path.exists(f'config/{guild.name}/settings.ini'):
            print('Config file exists, reading')
            cfg.config.read(f'config/{guild.name}/settings.ini')
        else:
            print('Config does not exist, creating')
            cfg.config[guild.name] = {
                'filterRole' : '',
                'filter' : [],
                'prefix' : '?',
                'loggingEnabled' : 'yes',
                'modrole' : ''
            }

            if not os.path.exists('config'):
                os.mkdir('config')

            os.mkdir(f'config/{guild.name}')
            with open(f'config/{guild.name}/settings.ini', 'w') as file:
                cfg.config.write(file)
            
        if not os.path.exists(f'logs/guilds/{guild.name}'):
            os.mkdir(f'logs/guilds/{guild.name}')

@cfg.bot.event
async def on_ready():
    print(f'{cfg.bot.user} has logged in to Discord!')
    await cfg.bot.change_presence(activity=discord.Game(name='with catgirls'))

    await connected()

    # log startup
    f = open(f'logs/startup/startup.log', 'a')
    f.write(f'{str(datetime.now())} {cfg.bot.user} is now online in {len(cfg.bot.guilds)} guilds!\n')
    f.close

    print(f'Successfully logged in and booted!')
    print(f'Bot is ready!')
    print('') # newline

@cfg.bot.event
async def on_connect():
    print(f'Connected to discord!')
    await connected()
    # connected
    print('') # newline


cfg.bot.run(os.getenv('DISCORD_TOKEN'), bot=True, reconnect=True)