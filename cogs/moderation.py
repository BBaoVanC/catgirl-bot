import discord
import cfg, owouwu
from discord.ext import commands

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
        print('Cog "Moderation" loaded')

    @commands.command(name='kick')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def kick(self, ctx, member=None, *reason_words):
        """Kick the mentioned member"""

        reason = ""
        if len(reason_words) == 0:
            reason = ' No reason'
        else:
            for word in reason_words:
                reason = f'{reason} {word}'

        async def kick(mem) -> bool:
            try:
                try:
                    await mem.send(f'{owouwu.gen()}, you have been kicked from {ctx.guild.name} for reason:{reason}')
                except:
                    print(f'Failed to message member {mem.name}')
                    await ctx.send(f'Failed to message member {mem.name}')
                await mem.kick()
            except:
                print(f'Failed to kick member {mem.name}')
                await ctx.send(f'Failed to kick member {mem.name}')
                return False 
            return True

        # mentions
        if ctx.message.mentions:
            for mem in ctx.message.mentions:
                # perform
                done = await kick(mem)
        else:
            # tag
            if(is_integer(member)):
                mem = await cfg.bot.fetch_user(int(member))
                done = await kick(mem)
        
        if not done:
            return

        await ctx.send(f'{owouwu.gen()}, 1 member kicked', delete_after=5)
        print(f'1 member kicked in {ctx.guild.id} ({ctx.guild.name})')
        await ctx.message.add_reaction('✅')

    @commands.command(name='ban')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def ban(self, ctx, member=None, *reason_words):
        """Ban the mentioned member"""

        reason = ""
        if len(reason_words) == 0:
            reason = ' No reason'
        else:
            for word in reason_words:
                reason = f'{reason} {word}'

        async def ban(mem) -> bool:
            try:
                try:
                    await mem.send(f'{owouwu.gen()}, you have been banned from {ctx.guild.name} for reason:{reason}')
                except:
                    print(f'Failed to message member {mem.name}')
                    await ctx.send(f'Failed to message member {mem.name}')
                await ctx.guild.ban(mem)
            except:
                print(f'Failed to ban member {mem.name}')
                await ctx.send(f'Failed to ban member {mem.name}')
                return False
            return True

        # mentions
        if ctx.message.mentions:
            for mem in ctx.message.mentions:
                # perform
                done = await ban(mem)
        else:
            # tag
            if(is_integer(member)):
                mem = await cfg.bot.fetch_user(int(member))
                done = await ban(mem)

        if not done:
                return

        await ctx.send(f'{owouwu.gen()}, 1 member banned', delete_after=5)
        print(f'1 member banned in {ctx.guild.id} ({ctx.guild.name})')
        await ctx.message.add_reaction('✅')

    @commands.command(name='warn')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def warn(self, ctx, member=None, *reason_words):
        """Warn the mentioned member"""

        reason = ""
        if len(reason_words) == 0:
            reason = ' No reason'
        else:
            for word in reason_words:
                reason = f'{reason} {word}'

        async def warn(mem) -> bool:
            try:
                await mem.send(f'{owouwu.gen()}, you have been warned from the moderators of {ctx.guild.name} for reason:{reason}. \n\nIf you continue to break the rules, you may be kicked or banned.')
            except:
                print(f'Failed to message member {mem.name}')
                await ctx.send(f'Failed to message member {mem.name}')
                return False
            return True

        # mentions
        if ctx.message.mentions:
            for mem in ctx.message.mentions:
                # perform
                done = await warn(mem)
        else:
            # tag
            if(is_integer(member)):
                mem = await cfg.bot.fetch_user(int(member))
                done = await warn(mem)

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
        messages = await ctx.channel.purge(limit=int(num))
        await ctx.send(f'Deleted {len(messages)} message(s), {owouwu.gen()}', delete_after=5)
        print(f'{len(messages)} messages purged from {ctx.message.channel.name} in {ctx.guild.id} ({ctx.guild.name})')


# add cog
def setup(bot):
    bot.add_cog(Moderation(bot))
    