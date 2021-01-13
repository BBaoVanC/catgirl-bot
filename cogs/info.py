#!/usr/bin/env python3
# info.py
# basic commands for information related to the bot and system
import discord, cfg, os, sys, threading, time, owouwu, debug
from discord.ext import commands
from discord.utils import oauth_url
from dotenv import load_dotenv
from timeformat import format_time
from psutil import virtual_memory, cpu_percent
from cooldown import cooldown

# start a stopwatch of sorts
boot_time = time.time()

class Info(commands.Cog):
    """Info"""

    def __init__(self, bot):
        self.bot = bot
        self.cooldown = cooldown(2)
        load_dotenv()

    # link source code (that's this!!!)
    @commands.command(name='github', aliases=['source', 'sourcecode'])
    async def link_github(self, ctx):
        '''The link to the source code OwO'''
        embed = discord.Embed(title='Source code',
                              description='The source code of this bot',
                              colour=0xFB98FB,
                              url='https://github.com/Burrit0z/catgirl-bot')
        embed.set_author(name=f'Catgirl Bot',
                         url='https://github.com/Burrit0z/',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=500')
        embed.set_image(url='https://avatars0.githubusercontent.com/u/57574731?s=500g')
        embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')

        await ctx.send(content=f'**Catgirl bot source code {owouwu.gen()}**', embed=embed)

    # get avatar
    @commands.command(name='avatar', aliases=['pfp'])
    async def get_avatar(self, ctx, *, tag=None):
        """Gets the avatar of a user, by mention or ID"""

        if not await self.cooldown.check_and_warn_usage(ctx.channel):
            return
        self.cooldown.was_used(ctx.guild.id)

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

        if not await self.cooldown.check_and_warn_usage(ctx.channel):
            return
        self.cooldown.was_used(ctx.guild.id)

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
        embed.set_author(name=f'Catgirl Bot',
                         url='https://github.com/Burrit0z/catgirl-bot',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=500')
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
        embed.set_author(name=f'Catgirl Bot',
                         url='https://github.com/Burrit0z/catgirl-bot',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=500')
        embed.set_image(url='https://raw.githubusercontent.com/Burrit0z/catgirl-bot/master/catgirl.png')
        await ctx.send(content=f'**Here is the invite link {owouwu.gen()}\n{url}**', embed=embed)

    # system info
    @commands.command(name='sysinfo', aliases=['stats'])
    async def send_stats(self, ctx):
        """Sends system info!"""

        # cooldown check, this command fetches lots of info
        if not await self.cooldown.check_and_warn_usage(ctx.channel):
            return
        self.cooldown.was_used(ctx.guild.id)

        # define function to round bytes to GiB (not GB)
        def rounded_gib(bytes) -> int:
            return round(bytes/1073741824, 1)

        if os.getenv('DEBUG') == 'yes':
            embed_title = 'Catgirl Bot - System info - DEBUG'
        else:
            embed_title = 'Catgirl Bot - System info'

        # variables for use later
        memory = virtual_memory()
        vi = sys.version_info
        combined_version = f'{vi.major}.{vi.minor}.{vi.micro}'

        # create and basic setup
        embed = discord.Embed(colour=0xFB98FB)
        embed.set_author(name=embed_title,
                         url='https://github.com/Burrit0z/catgirl-bot',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=500')
        embed.set_footer(text=f'Requested by {ctx.message.author.name}')

        # add fields
        embed.add_field(name="Python version", value=combined_version)
        embed.add_field(name="Uptime", value=format_time(time.time() - boot_time))
        embed.add_field(name="Ping", value=f'{round(cfg.bot.latency * 1000, 2)}ms')
        embed.add_field(name="Total Memory", value=f'{rounded_gib(memory.total)}GiB')
        embed.add_field(name="Memory Used", value=f'{rounded_gib(memory.used)}GiB ({memory.percent}%)')
        embed.add_field(name="Free Memory", value=f'{rounded_gib(memory.free)}GiB')
        embed.add_field(name="CPU Used", value=f'{round(cpu_percent(interval=1), 2)}%')

        # debug labels
        if os.getenv('DEBUG') == 'yes':
            embed.add_field(name="Bot Active Threads", value=threading.active_count())
            embed.add_field(name="Bot Current Thread", value=threading.current_thread().name)

        # send the finished product
        await ctx.send(content=f'Here you go {owouwu.gen()}', embed=embed)


    # take snapshot, for debug purposes only
    @commands.command(name='takesnap', hidden=True)
    @commands.is_owner()
    @commands.check(cfg.debug_enabled)
    async def take_snap(self, ctx):
        """Takes a snapshot of python's memory useage and prints some info to the console"""
        debug.snap()
        await ctx.send(f'Snapshot successfully taken {owouwu.gen()}')

    # just uptime
    @commands.command(name='uptime')
    async def send_uptime(self, ctx):
        """Sends current bot uptime!"""

        embed = discord.Embed(colour=0xFB98FB)
        embed.set_author(name=f'Catgirl Bot',
                         url='https://github.com/Burrit0z/catgirl-bot',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=500')
        embed.add_field(name="Uptime", value=format_time(time.time() - boot_time), inline=False)

        await ctx.send(content=f'{owouwu.gen()} current bot uptime', embed=embed)

     # system info
    @commands.command(name='ping')
    async def send_ping(self, ctx):
        """Sends current ping!"""

        if not await self.cooldown.check_and_warn_usage(ctx.channel):
            return
        self.cooldown.was_used(ctx.guild.id)

        embed = discord.Embed(colour=0xFB98FB)
        embed.set_author(name=f'Catgirl Bot',
                         url='https://github.com/Burrit0z/catgirl-bot',
                         icon_url='https://avatars0.githubusercontent.com/u/57574731?s=500')
        embed.add_field(name="Ping", value=f'{round(cfg.bot.latency * 1000, 2)}ms', inline=False)

        await ctx.send(content=f'{owouwu.gen()} current ping', embed=embed)

# add cog
def setup(bot):
    bot.add_cog(Info(bot))
    