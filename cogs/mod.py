import discord
import cfg
from discord.ext import commands

class Moderation(commands.Cog): 
    """Moderation"""

    def __init__(self, bot):
        self.bot = bot
        print('Cog "Moderation" loaded')

    @commands.command(name='kick')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def kick(self, ctx, *, reason="No reason"):
        """Kick all mentioned members"""

        if not ctx.message.mentions:
            await ctx.send(f'Usage: kick user reason (optional)', delete_after=5)
            return

        members = ctx.message.mentions
        for mem in members:
            try:
                await mem.send(f'You have been kicked from {ctx.guild.name} for reason: {reason}')
                await ctx.guild.kick(mem)
            except:
                print(f'Failed to kick member {mem.name}')
        
        await ctx.send(f'Members kicked', delete_after=5)
        await ctx.message.add_reaction('✅')

    @commands.command(name='ban')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def ban(self, ctx, *, reason="No reason"):
        """Ban all mentioned members"""

        if not ctx.message.mentions:
            await ctx.send(f'Usage: kick user reason (optional)', delete_after=5)
            return

        members = ctx.message.mentions
        for mem in members:
            try:
                await mem.send(f'You have been banned from {ctx.guild.name} for reason: {reason}')
                await ctx.guild.ban(mem)
            except:
                print(f'Failed to ban member {mem.name}')

        await ctx.send(f'Members banned', delete_after=5)
        await ctx.message.add_reaction('✅')

    @commands.command(name='warn')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def warn(self, ctx, *, reason="No reason"):
        """Warn all mentioned members"""

        if not ctx.message.mentions:
            await ctx.send(f'Usage: kick user reason (optional)', delete_after=5)
            return

        members = ctx.message.mentions
        for mem in members:
            try:
                await mem.send(f'You have been warned from the moderators of {ctx.guild.name} for reason: {reason}. \n\nIf you continue to break the rules, you may be kicked or banned.')
            except:
             print(f'Failed to warn member {mem.name}')

        await ctx.send(f'Members warned', delete_after=5)
        await ctx.message.add_reaction('✅')

    
    @commands.command(name='purge')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def purge(self, ctx, *, num=None):
        """Purge a certain number of messages"""
    
        if not num:
            await ctx.send(f'Usage: purge number', delete_after=5)
            return
        messages = await ctx.channel.purge(limit=int(num))
        await ctx.send(f'Deleted {len(messages)} message(s)', delete_after=5)


# add cog
def setup(bot):
    bot.add_cog(Moderation(bot))