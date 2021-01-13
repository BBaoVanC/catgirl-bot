#!/usr/bin/env python3
# cfg.py
# variables that need to be accesed globally, as well as command check function defs
import discord, configparser, os
from discord import DMChannel
from discord.ext import commands
from dotenv import load_dotenv

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

# config
config = configparser.ConfigParser()


# get bot prefix
def get_prefix(bot, message):

    # not dm, get config, otherwise fallback
    if not isinstance(message.channel, DMChannel):
        guild_prefix = config[str(message.channel.guild.id)]['prefix']
    else:
        guild_prefix = "?"

    prefixes = [str(guild_prefix)]

    return commands.when_mentioned_or(*prefixes)(bot, message)

# can the user perform the command?
async def hasperms(ctx):
    user = ctx.message.author
    has_mod = False

    if isinstance(ctx.message.channel, DMChannel):
        return False # dm

    for role in user.roles:
        if int(role.id) == int(config[str(ctx.guild.id)]['modrole']):
            has_mod = True

    ret = user.guild_permissions.administrator or has_mod
    return ret


# are we in a guild?
async def isguild(ctx):
    return (not isinstance(ctx.message.channel, DMChannel))

async def debug_enabled(ctx):
    if os.getenv('DEBUG') == 'yes':
        return True
    else:
        return False

# setup intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, description='catgirl bot', intents=intents)
    