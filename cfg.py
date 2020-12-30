import configparser
import discord
from discord.ext import commands
from discord import Intents

def get_prefix(bot, message):

    prefixes = ['?']

    return commands.when_mentioned_or(*prefixes)(bot, message)

# config
config = configparser.ConfigParser()

# setup actual bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, description='catgirl bot', intents=intents)

async def hasperms(ctx):
    user = ctx.message.author
    has_mod = False

    for role in user.roles:
        if int(role.id) == int(config[ctx.guild.name]['modrole']):
            has_mod = True

    ret = user.guild_permissions.administrator or has_mod
    if not ret:
        await ctx.send(f'{user.mention}, you do not have permission to use this command! OwO')
    return ret

def isguild(ctx):
    return ctx.guild != None