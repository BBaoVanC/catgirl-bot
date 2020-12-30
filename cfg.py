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
    try:
        user = ctx.message.author
        ret = user.guild_permissions.administrator or config[f'ctx.guild.name']['modrole'] in user.roles
        if not ret:
            await ctx.send(f'{user.mention}, you do not have permission to use this command! OwO')
        return ret
    except:
        return False

def isguild(ctx):
    return ctx.message.guild != None