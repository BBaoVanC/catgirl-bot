import discord, os, json
import cfg, logger, filtercheck
from discord.ext import commands
from datetime import datetime
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

        if not input:
            await ctx.send(f'Usage: filter add/remove word', delete_after=5)
            return

        args = input.split()

        if(len(args) < 2):
            await ctx.send(f'Usage: filter add/remove word', delete_after=5)
            return
    
        filter = json.loads(cfg.config[f'{ctx.guild.id}']['filter'])
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
        cfg.config[f'{ctx.guild.id}']['filter'] = f'{filter}'.replace('\'','"')

        try:
            file = open(f'config/bot/settings.ini', 'w')
            cfg.config.write(file)
            file.close()
            if(args[0] == 'add'):
                await ctx.send(f'{len(words)} words added to filter', delete_after=5)
            elif(args[0] == 'remove'):
                await ctx.send(f'{len(words)} words removed from filter', delete_after=5)
            
            await ctx.message.add_reaction('✅')
        except:
            await ctx.send(f'Command failed to execute', delete_after=5)

    @commands.command(name='filterrole')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def set_role(self, ctx, *, role_id=None):
        """Set no filter role"""

        if not role_id:
            await ctx.send("Usage: filterrole role_id", delete_after=5)
            return

        try:
            role = ctx.guild.get_role(int(role_id))
            # save file
            cfg.config[f'{ctx.guild.id}']['filterrole'] = role_id
            try:
                file = open(f'config/bot/settings.ini', 'w')
                cfg.config.write(file)
                file.close()
            except:
                await ctx.send(f'Command failed to execute', delete_after=5)
        except:
            print(f'Role for ID {role_id} not found')
            return

        print(f'No filter role set to {ctx.guild.get_role(int(role_id))}')
        await ctx.send(f'No filter role set to "{ctx.guild.get_role(int(role_id))}"', delete_after=5)
        await ctx.message.add_reaction('✅')

    @commands.Cog.listener()
    async def on_message(self, message):
        # message context
        context = messagecontext(message)

        # get guild
        guild = context.guild()
        if guild:

            try:
                prefix = cfg.config[str(message.channel.guild.id)]['prefix']
            except:
                return
                print(f'Error handling message')

            # log message
            await logger.logChatMessage(context)
            # if it is the bot, or command, return
            if message.author == cfg.bot.user or message.content.startswith(prefix):
                pass
            else:
                await filtercheck.checkMessage(context)

# add cog
def setup(bot):
    bot.add_cog(Filter(bot))