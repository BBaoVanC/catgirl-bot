import discord, cfg
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

        cfg.config[f'{ctx.guild.name}']['prefix'] = prefix

        try:
            file = open(f'config/{ctx.guild.name}/settings.ini', 'w')
            cfg.config.write(file)
            file.close()
            
            await ctx.send(f'Prefix changed to "{prefix}')
            printd(f'Prefix changed to "{prefix}')
            await ctx.message.add_reaction('✅')
        except:
            await ctx.send(f'Command failed to execute', delete_after=5)


    # set moderator role
    @commands.command(name='modrole')
    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    async def set_prefix(self, ctx, *, role_id=None):
        """Set the role for moderators"""

        if not role_id:
            await ctx.send(f"Usage: modrole role_id", delete_after=5)
            return
        
        if not ctx.guild.get_role(int(role_id)):
            ctx.send(f"Role with that ID could not be found", delete_after=5)
            return

        cfg.config[f'{ctx.guild.name}']['modrole'] = role_id

        try:
            file = open(f'config/{ctx.guild.name}/settings.ini', 'w')
            cfg.config.write(file)
            file.close()
            
            await ctx.send(f'Moderator role changed to "{ctx.guild.get_role(int(role_id))}"')
            print(f'Moderator role changed to "{ctx.guild.get_role(int(role_id))}"')
            await ctx.message.add_reaction('✅')
        except:
            await ctx.send(f'Command failed to execute', delete_after=5)

# add cog
def setup(bot):
    bot.add_cog(Config(bot))