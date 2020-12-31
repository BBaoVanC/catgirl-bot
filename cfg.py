import configparser
import discord
from discord import DMChannel
from discord.ext import commands

# config
config = configparser.ConfigParser()

def get_prefix(bot, message):

    # not dm, get config, otherwise fallback
    if not isinstance(message.channel, DMChannel):
        guild_prefix = config[str(message.channel.guild.id)]['prefix']
    else:
        guild_prefix = "?"

    prefixes = [str(guild_prefix)]

    return commands.when_mentioned_or(*prefixes)(bot, message)

# setup actual bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, description='catgirl bot', intents=intents)

async def hasperms(ctx):
    user = ctx.message.author
    has_mod = False

    if isinstance(ctx.message.channel, DMChannel):
        return False # dm

    for role in user.roles:
        if int(role.id) == int(config[str(ctx.guild.id)]['modrole']):
            has_mod = True

    ret = user.guild_permissions.administrator or has_mod
    if not ret:
        await ctx.send(f'{user.mention}, you do not have permission to use this command! OwO')
    return ret

def isguild(ctx):
    return (not isinstance(ctx.message.channel, DMChannel))
