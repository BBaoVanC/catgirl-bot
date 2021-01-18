#!/usr/bin/env python3
# moderation.py
# basic moderation commands
import discord, cfg, owouwu, filemanager, os
from discord.ext import commands
from logger import send_discord_mod_log_message
from context import messagecontext

def is_integer(str):
    try: 
        int(str)
        return True
    except:
        return False

class Moderation(commands.Cog): 
    """Moderation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def kick(self, ctx, member=None, *reason):
        """Kick the mentioned member"""
        
        finalizedReason = ''
        if len(reason) == 0:
            finalizedReason = 'No reason'
        else:
            for word in reason:
                finalizedReason = f'{finalizedReason} {word}'

        async def kick(mem) -> bool:
            try:
                await mem.send(f'{owouwu.gen()}, you have been kicked from {ctx.guild.name} for reason:{finalizedReason}')
            except:
                print(f'Failed to message member {mem.name}')
                await ctx.send(f'Failed to message member {mem.name}', delete_after=5)

            try:
                await mem.kick()
                discord_message = {
                    'User' : mem.name,
                    'Reason' : finalizedReason,
                    'Moderator' : ctx.message.author
                }
                await send_discord_mod_log_message(messagecontext(ctx.message), mem, discord_message,'Member kicked')
            except:
                print(f'Failed to kick member {mem.name}')
                await ctx.send(f'Failed to kick member {mem.name}, do I have the correct permission to do so?', delete_after=5)
                return False 
            return True

        done = False
        mem = None

        # mentions
        if ctx.message.mentions:
            mem = ctx.message.mentions[0]
        else:
            # tag
            if(is_integer(member)):
                mem = await cfg.bot.fetch_user(int(member))

        # perform
        if mem != cfg.bot.user:
            done = await kick(mem)
        else:
            await ctx.send(f'But... that\'s me...')
        
        if not done:
            return

        await ctx.send(f'{owouwu.gen()}, 1 member kicked', delete_after=5)
        print(f'1 member kicked in {ctx.guild.id} ({ctx.guild.name})')
        await ctx.message.add_reaction('✅')

    @commands.command(name='ban')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def ban(self, ctx, member=None, *reason):
        """Ban the mentioned member"""

        finalizedReason = ''
        if len(reason) == 0:
            finalizedReason = 'No reason'
        else:
            for word in reason:
                finalizedReason = f'{finalizedReason} {word}'

        async def ban(mem) -> bool:
            try:
                await mem.send(f'{owouwu.gen()}, you have been banned from {ctx.guild.name} for reason:{finalizedReason}')
            except:
                print(f'Failed to message member {mem.name}')
                await ctx.send(f'Failed to message member {mem.name}', delete_after=5)

            try:
                await ctx.guild.ban(mem, reason=finalizedReason)
                print(f'{mem.name} - {mem.id} was banned from {ctx.guild.name} - {ctx.guild.id}')
                discord_message = {
                    'User' : mem.name,
                    'Reason' : finalizedReason,
                    'Moderator' : ctx.message.author
                }
                await send_discord_mod_log_message(messagecontext(ctx.message), mem, discord_message,'Member banned')
            except:
                print(f'Failed to ban member {mem.name}')
                await ctx.send(f'Failed to ban member {mem.name}, do I have the correct permission to do so?', delete_after=5)
                return False
            return True

        done = False
        mem = None

        # mentions
        if ctx.message.mentions:
            mem = ctx.message.mentions[0]
        else:
            # tag
            if(is_integer(member)):
                mem = await cfg.bot.fetch_user(int(member))

        # perform
        if mem != cfg.bot.user:
            done = await ban(mem)
        else:
            await ctx.send(f'But... that\'s me...')

        if not done:
            return

        await ctx.send(f'{owouwu.gen()}, 1 member banned', delete_after=5)
        print(f'1 member banned in {ctx.guild.id} ({ctx.guild.name})')
        await ctx.message.add_reaction('✅')

    @commands.command(name='warn')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def warn(self, ctx, member=None, *reason):
        """Warn the mentioned member"""

        finalizedReason = ''
        if len(reason) == 0:
            finalizedReason = 'No reason'
        else:
            for word in reason:
                finalizedReason = f'{finalizedReason} {word}'

        async def warn(mem) -> bool:
            try:
                await mem.send(f'{owouwu.gen()}, you have been warned from the moderators of {ctx.guild.name} for reason:{finalizedReason}. \n\nIf you continue to break the rules, you may be kicked or banned.')
                discord_message = {
                    'User' : mem.name,
                    'Reason' : finalizedReason,
                    'Moderator' : ctx.message.author
                }
                await send_discord_mod_log_message(messagecontext(ctx.message), mem, discord_message,'Member warned')
            except:
                print(f'Failed to message member {mem.name}')
                await ctx.send(f'Failed to message member {mem.name}', delete_after=5)
                return False
            return True

        done = False
        mem = None

        # mentions
        if ctx.message.mentions:
            mem = ctx.message.mentions[0]
        else:
            # tag
            if(is_integer(member)):
                mem = await cfg.bot.fetch_user(int(member))

        # perform
        if mem != cfg.bot.user:
            done = await warn(mem)
        else:
            await ctx.send(f'But... that\'s me...')

        if not done:
            return

        await ctx.send(f'{owouwu.gen()}, 1 member warned', delete_after=5)
        print(f'1 member warned in {ctx.guild.id} ({ctx.guild.name})')
        await ctx.message.add_reaction('✅')

    
    @commands.command(name='purge')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def purge(self, ctx, *, num=None):
        """Purge a certain number of messages"""
    
        if not num:
            await ctx.send(f'Usage: purge number', delete_after=5)
            return

        try:
            messages = await ctx.channel.purge(limit=int(num))
            await ctx.send(f'Deleted {len(messages)} message(s), {owouwu.gen()}', delete_after=5)
        except:
            await ctx.send(f'Could not purge messages, do I have permission to do so?', delete_after=5)

        print(f'{len(messages)} messages purged from {ctx.message.channel.name} in {ctx.guild.id} ({ctx.guild.name})')

    @commands.command(name='getlogs')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def get_logs(self, ctx):
        """Get a zip of all the logs the bot has collected from the server"""

        guild = ctx.guild
        zip_path = await filemanager.make_zip_file(guild)

        print(f'Logs requested for guild: {guild.name}-{guild.id}. Resulting temp file located at: {zip_path}')
        await ctx.send(content=f'Logs for guild **{ctx.guild.name}**', file=discord.File(zip_path))


# add cog
def setup(bot):
    bot.add_cog(Moderation(bot))
    