import discord, os, json
import cfg
from discord.ext import commands
from datetime import datetime

# define log function
async def logMessage(message):
    # write message to a file if the option is on
    enabled = True
    try:
        enabled = cfg.config.getboolean('SERVER', 'loggingEnabled')
    except:
        print('Could not convert the value of "loggingEnabled" to a boolean, defaulting to True')

    if enabled:
        try:
            # mkdir for guild if it doesnt exist
            if(os.path.exists(f'logs/messages/{message.channel.guild.name}') == False):
                os.mkdir(f'logs/messages/{message.channel.guild.name}')

            # open file and write 
            f = open(f'logs/messages/{message.channel.guild.name}/{message.channel.name}.log', 'a')
            f.write(f'\n{str(datetime.now())} {message.author.display_name}({message.author.name}): {message.content}\n')
            f.close
        except:
            f = open(f'logs/{message.channel.name}.log', 'a')
            f.write(f'\n{str(datetime.now())} {message.author.display_name}({message.author.name}): Unable to log contents, exception occured\n')
            f.close

# define message check function
# checks against filter and some other things
async def checkMessage(guild, message):

    # split message into an array to check individual words
    words = message.content.lower().split()
    
    # react
    if 'catgirl' in words or 'neko' in words or 'sex' in words:
        await message.add_reaction('<:wooaaahhh:789297106837569557>') #wooaaahhh
    
    # pedo
    elif ('cp' in words) or ('child' in words and 'porn' in words):
        try:
            await message.delete()
            await message.author.kick()
            await message.channel.send(f'{message.author.name} has been kicked for being a literal pedo')
        except:
            print(f'Error kicking user {message.author.name}! Does bot have correct permissions to kick this user?')
   
    # check filters
    else:
        # exempt users with no filter role
        try:
            if guild.get_role(cfg.config.getint('SERVER', 'filterrole')) in message.author.roles:
                return
        except:
            print('No filter role is not set!')

        # enumerate through
        # json load to make it a list
        for word in json.loads(cfg.config['SERVER']['filter']):
            if word in words:
                await message.channel.send(content=f'{message.author.mention}, that word is not allowed here!', delete_after=10)
                try:
                    await message.delete()
                except:
                    print('Failed to delete message.')

class FilterCog(commands.Cog): 
    """FilterCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='filter')
    async def filter_command(self, ctx, *, input=None):
        """Adjust filtered words"""

        args = input.split()

        if(len(args) < 2):
            await ctx.send(f'Usage: filter add/remove word', delete_after=5)
            return
    
        filter = json.loads(cfg.config['SERVER']['filter'])
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
        cfg.config['SERVER']['filter'] = f'{filter}'.replace('\'','"')

        try:
            file = open('config/bot/settings.ini', 'w')
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
    async def set_role(self, ctx, *, role_id=None):
        """Set no filter role"""

        if not role_id:
            await ctx.send("Usage: filterrole role_id", delete_after=5)
            return

        try:
            role = ctx.guild.get_role(int(role_id))
            # save file
            cfg.config['SERVER']['filterrole'] = role_id
            try:
                file = open('config/bot/settings.ini', 'w')
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
'''
    @commands.Cog.listener()
    async def on_message(self, ctx):
        print(type(ctx))
        # get guild
        try:
            guild = ctx.guild
        except:
            # not guild
            return

        # log message
        await logMessage(ctx)

        # if it is the bot, return
        if ctx.author == bot.user:
            return
        
        checkMessage(ctx.guild, ctx)'''

# add cog
def setup(bot):
    bot.add_cog(FilterCog(bot))