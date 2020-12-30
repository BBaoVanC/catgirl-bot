import discord, cfg
from discord.ext import commands

class Base(commands.Cog):
    """Base"""

    def __init__(self, bot):
        self.bot = bot
        print('Cog "Base" loaded')

    @commands.command(name='say', aliases=['copy', 'mimic'])
    async def say_command(self, ctx, *, our_input: str):
        """Says what you tell me to!"""

        if '@' in our_input and '<' in our_input and '>' in our_input or '@everyone' in our_input or '@here' in our_input:
            await ctx.send('I cannot mention users!', delete_after=5)
            return

        await ctx.send(our_input)

    @commands.command(name='hello')
    @commands.is_owner()
    async def hello_command(self, ctx):
        """UwU"""

        await ctx.send(f'Hello master! UwU')

    # link source code (that's this!!!)
    @commands.command(name='github', aliases=['source', 'sourcecode'])
    async def link_github(self, ctx):
        embed = discord.Embed(title='Source code',
                              description='The source code of this bot',
                              colour=0xFB98FB,
                              url='https://github.com/Burrit0z/catgirl-bot')
        embed.set_author(name='Catgirl Bot',
                         url='https://github.com/Burrit0z/',
                         icon_url='https://avatars1.githubusercontent.com/u/57574731?s=460&u=1ed4b749c9487d2f4160c7060e149172714ee18f&v=4')
        embed.set_image(url='https://avatars1.githubusercontent.com/u/57574731?s=460&u=1ed4b749c9487d2f4160c7060e149172714ee18f&v=4g')
        embed.set_footer(text='Made in Python with discord.py@rewrite', icon_url='http://i.imgur.com/5BFecvA.png')

        await ctx.send(content='**Catgirl bot source code UwU**', embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        print(f'{user.name}-{user.id} was banned from {guild.name}-{guild.id}')
    

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
                await ctx.send(f"Failed to get user avatar, did you provide a valid ID?", delete_after=5)
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
                await ctx.send(f"Failed to get user, did you provide a valid ID?", delete_after=5)
                return
        else:
            user = ctx.message.author

        embed = discord.Embed(colour=0xFB98FB)
        embed.set_author(name='Catgirl Bot',
                         url='https://github.com/Burrit0z/',
                         icon_url='https://avatars1.githubusercontent.com/u/57574731?s=460&u=1ed4b749c9487d2f4160c7060e149172714ee18f&v=4')
        embed.add_field(name="Display Name", value=user.display_name)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Created", value=user.created_at)
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(content=f'**User info for "{user.name}"**', embed=embed)

# add cog
def setup(bot):
    bot.add_cog(Base(bot))