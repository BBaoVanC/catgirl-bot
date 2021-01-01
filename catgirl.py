#!/usr/bin/env python3
# catgirl.py
# main file for catgirl bot
import discord, sys, os
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(1, 'mod')
sys.path.insert(1, 'data')
from logger import write_log_message
from filemanager import make_dir_if_needed
import cfg, settings

load_dotenv()

# cog list
cogs = [
    'cogs.info',
    'cogs.filter',
    'cogs.moderation',
    'cogs.config',
    'cogs.messagetrack'
]

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    print(f'Loading {len(cogs)} cogs!')

    for extension in cogs:
        cfg.bot.load_extension(extension)
    
    print('') # newline

async def connected():

    # log folder
    make_dir_if_needed('tmp')
    make_dir_if_needed('logs')
    make_dir_if_needed('logs/botevent')
    make_dir_if_needed('logs/guilds')

    # read config file once
    if os.path.exists(f'config/bot/settings.ini'):
        cfg.config.read(f'config/bot/settings.ini')

    # setup for each guild
    for guild in cfg.bot.guilds:
        if guild.name == None:
            return

        # does file exist?
        if os.path.exists(f'config/bot/settings.ini'):

            # if config for guild not existing, create
            if not str(guild.id) in cfg.config.sections():
                print(f'Config does not exist for guild {guild.id} ({guild.name}), creating')
                cfg.config[guild.id] = settings.default_config()

                # write changes
                settings.save_config()
            else:
                print(f'Config exists for guild {guild.id} ({guild.name})')
        else:
            # create
            print(f'Main config file does not exist, creating')
            cfg.config[guild.id] = settings.default_config()

            make_dir_if_needed(f'config')
            make_dir_if_needed(f'config/bot')
            settings.save_config()
        
        # make logs for each guild
        make_dir_if_needed(f'logs/guilds/{guild.id}')

@cfg.bot.event
async def on_ready():
    print(f'{cfg.bot.user} has logged in to Discord!')
    await cfg.bot.change_presence(activity=discord.Game(name='with catgirls'))

    await connected()

    # log botevent
    botevent_log = f'logs/botevent/botevent.log'
    message = f'{str(datetime.now())} {cfg.bot.user} is now online in {len(cfg.bot.guilds)} guilds!\n'
    write_log_message(message, botevent_log)

    print(f'Successfully logged in and booted!')
    print(f'{cfg.bot.user} is now online in {len(cfg.bot.guilds)} guilds!')
    print(f'Bot is ready!')
    print('') # newline

@cfg.bot.event
async def on_guild_join(guild):
    # force reload config and logs
    await connected()

    # log botevent
    botevent_log = f'logs/botevent/botevent.log'
    message = f'{str(datetime.now())} {cfg.bot.user} joined the guild {guild.id} ({guild.name})!\n'
    write_log_message(message, botevent_log)

    print(f'\nJoined the guild {guild.id} ({guild.name})!\n')

@cfg.bot.event
async def on_guild_remove(guild):
    # log botevent
    botevent_log = f'logs/botevent/botevent.log'
    message = f'Left the guild {guild.id} ({guild.name})!\n'
    write_log_message(message, botevent_log)

    print(f'\nLeft the guild {guild.id} ({guild.name})!\n')

cfg.bot.run(os.getenv('DISCORD_TOKEN'), bot=True, reconnect=True)
