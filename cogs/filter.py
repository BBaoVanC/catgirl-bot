#!/usr/bin/env python3
# filter.py
# deals with content based filter settings
import discord, json
import cfg, logger, filtercheck, owouwu, settings
from discord.ext import commands
from context import messagecontext

class Filter(commands.Cog): 
    """Filter"""

    def __init__(self, bot):
        self.bot = bot
        print('Cog "Filter" loaded')

    @commands.command(name='filter')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def filter_command(self, ctx, *, input=None):
        """Adjust filtered words"""

        guild_id = ctx.guild.id

        if not input:
            await ctx.send(f'Usage: filter add/remove word', delete_after=5)
            return

        args = input.split()

        if(len(args) < 2):
            await ctx.send(f'Usage: filter add/remove word', delete_after=5)
            return
    
        filter = json.loads(settings.get_value(guild_id, 'filter'))
        words = input.split()
        del words[0] # delete the first term, the "operand"

        if(args[0] == 'add'):
            for word in words:
                filter.append(word)
        elif(args[0] == 'remove'):
            for word in words:
                filter.remove(word)
        else:
            await ctx.send(f'Usage: filter add/remove word word word', delete_after=5)
            return

        # save the file, convert the ' to " first, since json dies
        settings.set_value(guild_id, 'filter', f'{filter}'.replace('\'','"'))

        try:
            settings.save_config()

            if(args[0] == 'add'):
                await ctx.send(f'{len(words)} words added to filter, {owouwu.gen()}', delete_after=5)
            elif(args[0] == 'remove'):
                await ctx.send(f'{len(words)} words removed from filter, {owouwu.gen()}', delete_after=5)
            
            await ctx.message.add_reaction('✅')
        except:
            await ctx.send(f'Command failed to execute', delete_after=5)

    @commands.command(name='filterrole')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def set_role(self, ctx, *, role_id=None):
        """Set no filter role"""

        guild_id = ctx.guild.id

        if not role_id:
            await ctx.send("Usage: filterrole role_id", delete_after=5)
            return

        try:
            role = ctx.guild.get_role(int(role_id))
            # save file
            settings.set_value(guild_id, 'filterrole', role_id)
            try:
                settings.save_config()
            except:
                await ctx.send(f'Command failed to execute', delete_after=5)
        except:
            print(f'Role for ID {role_id} not found')
            await ctx.send(f'Role for ID {role_id} not found', delete_after=5)
            return

        print(f'No filter role set to {ctx.guild.get_role(int(role_id))} in guild {ctx.guild.name}-{guild_id}')
        await ctx.send(f'No filter role set to "{ctx.guild.get_role(int(role_id))}", {owouwu.gen()}', delete_after=5)
        await ctx.message.add_reaction('✅')

    @commands.Cog.listener()
    async def on_message(self, message):
        # message context
        context = messagecontext(message)

        # get guild
        guild = context.guild()
        if guild:

            try:
                prefix = settings.get_value(guild.id, 'prefix')
            except:
                return
                print(f'Error handling message')

            # log message
            await logger.logChatMessage(context)
            # if it is the bot, or command, return
            if message.author == cfg.bot.user:
                pass
            else:
                await filtercheck.checkMessage(context)

            if message.content.startswith(prefix):
                await logger.logCommandSent(context)

# add cog
def setup(bot):
    bot.add_cog(Filter(bot))
    