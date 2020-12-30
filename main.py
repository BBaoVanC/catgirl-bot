#!/usr/bin/env python3

import os
import discord
from datetime import datetime

# setup actual bot
bot = discord.Client()

# import funcs
import handlers
import custom

# core
class BotClient(discord.Client):
        
    # bot is ready
    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        await bot.change_presence(activity=discord.Game(name='with catgirls'))

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

        if message.content.startswith(custom.PREFIX):
            await handlers.checkCommands(guild, message)
        else:
            await handlers.checkMessage(guild, message)

bot.run(custom.TOKEN)