import configparser
import discord
from discord.ext import commands
from discord import Intents

# config
config = configparser.ConfigParser()

def get_prefix(bot, message):

    guild_prefix = config[message.channel.guild.id]['prefix']
    prefixes = [str(guild_prefix)]

    return commands.when_mentioned_or(*prefixes)(bot, message)

# setup actual bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, description='catgirl bot', intents=intents)

async def hasperms(ctx):
    user = ctx.message.author
    has_mod = False

    for role in user.roles:
        if int(role.id) == int(config[ctx.guild.id]['modrole']):
            has_mod = True

    ret = user.guild_permissions.administrator or has_mod
    if not ret:
        await ctx.send(f'{user.mention}, you do not have permission to use this command! OwO')
    return ret

def isguild(ctx):
    return ctx.guild != None