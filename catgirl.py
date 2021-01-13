#!/usr/bin/env python3
# catgirl.py
# main file for catgirl bot
import discord, sys, os

# check versions before continuing
if sys.version_info[0] < 3:
    raise Exception("Python 3 or higher is required for this bot! Recommended version: 3.9.1")

if int(discord.__version__[2]) < 5:
	raise Exception("Discord.py 1.5.0 or higher is required for this bot! Recommended version: 1.5.1")

from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(1, 'mod')
sys.path.insert(1, 'data')
from logger import write_log_message
from filemanager import make_dir_if_needed
import cfg, settings
from debug import start_run_loop

load_dotenv()

# cog list
cogs = [
    'cogs.info',
    'cogs.filter',
    'cogs.moderation',
    'cogs.config',
    'cogs.messagetrack',
    'cogs.misc',
    'cogs.image'
]

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':

    print(f'Loading {len(cogs)} cogs!')
    for extension in cogs:
        cfg.bot.load_extension(extension)

    if os.getenv('DEBUG') == 'yes':
        print('') # newline
        print('DEBUG IS ENABLED')
        print('Starting debug thread!')
        start_run_loop()
        
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
    await cfg.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="catgirls"))

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

    await guild.owner.send(f'Hello! Please make sure I have the permissions needed to send messages in your server, and to perform the commands you wish to use!')
    await guild.owner.send(f'That means if you wish to use my moderation commands, you should give me permissions to kick/ban members and adjust their roles!')
    await guild.owner.send(f'*If I do not have permissions to send messages in a channel, you will not get a warning, the output simply will not be sent.*')

@cfg.bot.event
async def on_guild_remove(guild):
    # log botevent
    botevent_log = f'logs/botevent/botevent.log'
    message = f'{str(datetime.now())} {cfg.bot.user} left the guild {guild.id} ({guild.name})!\n'
    write_log_message(message, botevent_log)

    print(f'\nLeft the guild {guild.id} ({guild.name})!\n')

cfg.bot.run(os.getenv('DISCORD_TOKEN'), bot=True, reconnect=True)
