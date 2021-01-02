#!/usr/bin/env python3
# info.py
# basic commands for information related to the bot and system
import discord, cfg, os, sys, time, owouwu, filtercheck
from context import messagecontext
from datetime import datetime
from discord.ext import commands
from discord.utils import oauth_url
from dotenv import load_dotenv
from timeformat import format_time
from logger import write_log_message
from psutil import virtual_memory

# start a stopwatch of sorts
boot_time = time.time()

class Info(commands.Cog):
    """Info"""

    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        print('Cog "Info" loaded')

    @commands.command(name='say', aliases=['copy', 'mimic'])
    async def say_command(self, ctx, *, our_input: str):
        """Says what you tell me to!"""

        if '@' in our_input and '<' in our_input and '>' in our_input or '@everyone' in our_input or '@here' in our_input:
            await ctx.send('I cannot mention users!', delete_after=5)
            return

        if await filtercheck.breaks_filter(messagecontext(ctx.message)):
            return

        await ctx.send(our_input)

    @commands.command(name='hello', hidden=True)
    @commands.is_owner()
    async def hello_command(self, ctx):
        """UwU"""

        await ctx.send(f'Hello master! {owouwu.gen()}')

    @commands.command(name='stopbot', hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown"""

        # log botevent
        botevent_log = f'logs/botevent/botevent.log'
        message = f'{str(datetime.now())} Shutting down!\n'
        write_log_message(message, botevent_log)

        await ctx.send(f'Going to sleep! {owouwu.gen()}')
        sys.exit()

    # link source code (that's this!!!)
    @commands.command(name='github', aliases=['source', 'sourcecode'])
    async def link_github(self, ctx):
        '''The link to the source code OwO'''
        embed = discord.Embed(title='Source code',
                              description='The source code of this bot',
                              colour=0xFB98FB,
                              url='https://github.com/Burrit0z/catgirl-bot')
        embed.set_author(name=f'Catgirl Bot {owouwu.gen()}',
                         url='https://github.com/Burrit0z/',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=460&u=3ab50d6fc0e3ccb4d6ced23ae2f80cbe82d9aaf0&v=4')
        embed.set_image(url='https://avatars0.githubusercontent.com/u/57574731?s=460&u=3ab50d6fc0e3ccb4d6ced23ae2f80cbe82d9aaf0&v=4g')
        embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')

        await ctx.send(content='**Catgirl bot source code UwU**', embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        print(f'{user.name} - {user.id} was banned from {guild.name} - {guild.id}')
    

    # get avatar
    @commands.command(name='avatar', aliases=['pfp'])
    async def get_avatar(self, ctx, *, tag=None):
        """Gets the avatar of a user, by mention or ID"""

        if ctx.message.mentions:
            url = ctx.message.mentions[0].avatar_url
        elif tag:
            try:
                user = await cfg.bot.fetch_user(int(tag))
                url = user.avatar_url
            except:
                await ctx.send(f"Failed to get user avatar, did you provide a valid ID? {owouwu.gen()}", delete_after=5)
                return
        else:
            url = ctx.message.author.avatar_url

        embed = discord.Embed(colour=0xFB98FB)
        embed.set_image(url=url)

        await ctx.send(embed=embed)

    # get user info
    @commands.command(name='userinfo', aliases=['info', 'user'])
    async def get_userinfo(self, ctx, *, tag=None):
        """Get user info, by mention or ID"""

        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        elif tag:
            try:
                user = await cfg.bot.fetch_user(int(tag))
            except:
                await ctx.send(f"Failed to get user, did you provide a valid ID? {owouwu.gen()}", delete_after=5)
                return
        else:
            user = ctx.message.author

        embed = discord.Embed(colour=0xFB98FB)
        embed.set_author(name=f'Catgirl Bot {owouwu.gen()}',
                         url='https://github.com/Burrit0z/catgirl-bot',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=460&u=3ab50d6fc0e3ccb4d6ced23ae2f80cbe82d9aaf0&v=4')
        embed.add_field(name="Display Name", value=user.display_name, inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Created", value=user.created_at, inline=False)
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(content=f'**{owouwu.gen()} user info for "{user.name}"**', embed=embed)


    # invite link for the current bot
    @commands.command(name='botinvite', aliases=['link'])
    async def get_link(self, ctx):
        """Get the invite link to add this bot to your server!"""
        url = oauth_url(os.getenv("CLIENT_ID"))

        embed = discord.Embed(colour=0xFB98FB)
        embed.set_author(name=f'Catgirl Bot {owouwu.gen()}',
                         url='https://github.com/Burrit0z/catgirl-bot',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=460&u=3ab50d6fc0e3ccb4d6ced23ae2f80cbe82d9aaf0&v=4')
        embed.set_image(url='https://raw.githubusercontent.com/Burrit0z/catgirl-bot/master/catgirl.png')
        await ctx.send(content=f'**Here is the invite link {owouwu.gen()}\n{url}**', embed=embed)

    # system info
    @commands.command(name='sysinfo', aliases=['stats'])
    async def send_stats(self, ctx):
        """Sends system info!"""
        memory = virtual_memory()

        def rounded_gb(bytes) -> int:
            return round(bytes/1073741824, 1)

        embed = discord.Embed(colour=0xFB98FB)
        embed.set_author(name=f'Catgirl Bot - System info {owouwu.gen()}',
                         url='https://github.com/Burrit0z/catgirl-bot',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=460&u=3ab50d6fc0e3ccb4d6ced23ae2f80cbe82d9aaf0&v=4')
        embed.add_field(name="Python version", value=sys.version, inline=False)
        embed.add_field(name="Uptime", value=format_time(time.time() - boot_time), inline=False)
        embed.add_field(name="Ping", value=f'{round(cfg.bot.latency * 1000, 2)}ms', inline=False)
        embed.add_field(name="Total Memory", value=f'{rounded_gb(memory.total)}GiB', inline=False)
        embed.add_field(name="Memory Used", value=f'{rounded_gb(memory.used)}GiB ({memory.percent}%)', inline=False)
        embed.add_field(name="Free Memory", value=f'{rounded_gb(memory.free)}GiB', inline=False)

        await ctx.send(content=f'Here you go {owouwu.gen()}', embed=embed)

     # system info
    @commands.command(name='ping')
    async def send_ping(self, ctx):
        """Sends current ping!"""

        embed = discord.Embed(colour=0xFB98FB)
        embed.set_author(name=f'Catgirl Bot {owouwu.gen()}',
                         url='https://github.com/Burrit0z/catgirl-bot',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=460&u=3ab50d6fc0e3ccb4d6ced23ae2f80cbe82d9aaf0&v=4')
        embed.add_field(name="Ping", value=f'{round(cfg.bot.latency * 1000, 2)}ms', inline=False)

        await ctx.send(content=f'{owouwu.gen()} current ping', embed=embed)

# add cog
def setup(bot):
    bot.add_cog(Info(bot))
    