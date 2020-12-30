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