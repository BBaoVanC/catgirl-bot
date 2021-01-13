#!/usr/bin/env python3
# misc.py
# random assorted commands that don't fit into any category
import discord, cfg, owouwu, filtercheck, random, json
from urllib.request import Request, urlopen
from  discord.ext import commands
from context import messagecontext

class Misc(commands.Cog):
    """Misc"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello', hidden=True)
    @commands.is_owner()
    async def hello_command(self, ctx):
        """UwU"""

        await ctx.send(f'Hello master! {owouwu.gen()}')
        
    @commands.check(cfg.isguild)
    @commands.command(name='say', aliases=['copy', 'mimic'])
    async def say_command(self, ctx, *, message: str):
        """Makes me say what you tell me to!"""

        if '@' in message and '<' in message and '>' in message or '@everyone' in message or '@here' in message:
            await ctx.send('I cannot mention users!', delete_after=5)
            return

        if await filtercheck.breaks_filter(messagecontext(ctx.message)):
            return

        await ctx.send(message)

    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    @commands.command(name='sayembed')
    async def send_embed(self, ctx, title: str, *content: str):
        """Sends a embed with the given title and content. Intended for use by moderators in the rules channel."""

        if not title:
            await ctx.send('Usage: sayembed title content', delete_after=5)
            return

        if content:
            # turn content from a list into a string
            desc = ' '.join(content)
        else:
            desc = ''

        embed = discord.Embed(description=desc, title=title, colour=0xFB98FB)

        await ctx.send(embed=embed)
        await ctx.message.delete()

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

    @commands.command(name='status', hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx, *, status: str="catgirls"):
        """Sets bot status"""

        await cfg.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

# add cog
def setup(bot):
    bot.add_cog(Misc(bot))
