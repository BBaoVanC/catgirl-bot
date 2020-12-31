import cfg
from mod import owouwu
from discord.ext import commands

class Config(commands.Cog):
    """Config"""

    def __init__(self, bot):
        self.bot = bot
        print('Cog "Config" loaded')

    # set prefix
    @commands.command(name='prefix')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def set_prefix(self, ctx, *, prefix=None):
        """Set the prefix for all commands"""

        if not prefix:
            await ctx.send(f"Usage: prefix prefix", delete_after=5)
            return

        cfg.config[f'{str(ctx.guild.id)}']['prefix'] = prefix

        try:
            file = open(f'config/bot/settings.ini', 'w')
            cfg.config.write(file)
            file.close()
            
            await ctx.send(f'Prefix changed to "{prefix}')
            print(f'Prefix for {ctx.guild.id} ({ctx.guild.name}) changed to "{prefix}"')
            await ctx.message.add_reaction('✅')
        except:
            await ctx.send(f'Command failed to execute', delete_after=5)


    # set moderator role
    @commands.command(name='modrole')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def set_modrole(self, ctx, *, role_id=None):
        """Set the role for moderators"""

        if not role_id:
            await ctx.send(f"Usage: modrole role_id", delete_after=5)
            return
        
        if not ctx.guild.get_role(int(role_id)):
            ctx.send(f"Role with that ID could not be found", delete_after=5)
            return

        cfg.config[f'{str(ctx.guild.id)}']['modrole'] = role_id

        try:
            file = open(f'config/bot/settings.ini', 'w')
            cfg.config.write(file)
            file.close()
            
            await ctx.send(f'Moderator role changed to "{ctx.guild.get_role(int(role_id))}", {owouwu.gen()}')
            print(f'Moderator role for {ctx.guild.id} ({ctx.guild.name}) changed to "{ctx.guild.get_role(int(role_id))}"')
            await ctx.message.add_reaction('✅')
        except:
            await ctx.send(f'Command failed to execute', delete_after=5)

# add cog
def setup(bot):
    bot.add_cog(Config(bot))
