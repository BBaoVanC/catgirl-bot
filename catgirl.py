import discord, sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(1, 'mod')
sys.path.insert(1, 'data')
import os
import cfg, logger

load_dotenv()

# cog list
cogs = [
    'cogs.basic',
    'cogs.filter',
    'cogs.moderation',
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

        # does file exist?
        if os.path.exists(f'config/bot/settings.ini'):
            cfg.config.read(f'config/bot/settings.ini')

            # if config for guild not existing, create
            if not str(guild.id) in cfg.config.sections():
                print(f'Config does not exist for guild {guild.id} ({guild.name}), creating')
                cfg.config[guild.id] = {
                    'filterRole' : '1', # so none, but store an int
                    'filter' : [],
                    'prefix' : '?',
                    'loggingEnabled' : 'yes',
                    'modrole' : '1' # same here
                }

                # write changes
                with open(f'config/bot/settings.ini', 'w') as file:
                    cfg.config.write(file)
            else:
                print(f'Config exists for guild {guild.id} ({guild.name})')
        else:
            # create
            print(f'Main config file does not exist, creating')
            cfg.config[guild.id] = {
                'filterRole' : '1',
                'filter' : [],
                'prefix' : '?',
                'loggingEnabled' : 'yes',
                'modrole' : '1'
            }

            if not os.path.exists('config'):
                os.mkdir('config')

            os.mkdir(f'config/bot')
            with open(f'config/bot/settings.ini', 'w') as file:
                cfg.config.write(file)
        
        # make logs for each guild
        if not os.path.exists(f'logs/guilds/{guild.id}'):
            os.mkdir(f'logs/guilds/{guild.id}')

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
    print(f'{cfg.bot.user} is now online in {len(cfg.bot.guilds)} guilds!')
    print(f'Bot is ready!')
    print('') # newline

@cfg.bot.event
async def on_guild_join(guild):
    # force reload config and logs
    await connected()

    # log startup
    f = open(f'logs/startup/startup.log', 'a')
    f.write(f'{str(datetime.now())} {cfg.bot.user} joined the guild {guild.id} ({guild.name})!\n')
    f.close

    print(f'\nJoined the guild {guild.id} ({guild.name})!\n')

@cfg.bot.event
async def on_guild_remove(guild):
    print(f'\nLeft the guild {guild.id} ({guild.name})!\n')

cfg.bot.run(os.getenv('DISCORD_TOKEN'), bot=True, reconnect=True)