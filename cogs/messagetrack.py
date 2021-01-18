#!/usr/bin/env python3
# messagetrack.py
# track changes in existing messages and log them
import discord, logger, filtercheck
from discord.ext import commands
from context import messagecontext

class MessageTrack(commands.Cog):
    """MessageTrack"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, oldmessage, newmessage):
        old_context = messagecontext(oldmessage)
        new_context = messagecontext(newmessage)

        # get guild
        guild = old_context.guild()
        if guild:
            await filtercheck.checkMessage(new_context)
            await logger.logMessagedAltered(old_context, new_context)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        context = messagecontext(message)

        # get guild
        guild = context.guild()
        if guild:
            await logger.logMessagedDeleted(context)

# add cog
def setup(bot):
    bot.add_cog(MessageTrack(bot))
