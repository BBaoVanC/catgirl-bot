import discord
from discord.ext import commands

class BasicCog(commands.Cog):
    """BasicCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='say', aliases=['copy', 'mimic'])
    async def say_command(self, ctx, *, our_input: str):

        await ctx.send(our_input)

    @commands.command(name='hello')
    @commands.is_owner()
    async def hello_command(self, ctx):
        """UwU"""

        await ctx.send(f'Hello master! UwU')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        print(f'{user.name}-{user.id} was banned from {guild.name}-{guild.id}')

# add cog
def setup(bot):
    bot.add_cog(BasicCog(bot))