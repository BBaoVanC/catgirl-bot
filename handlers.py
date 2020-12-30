import cfg

import os
import json
from datetime import datetime

import cmd

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

# check for the commnands to execute
async def checkCommands(guild, message):
    
    # split into args
    args = message.content.lower().split()
    prefix = cfg.config['SERVER']['prefix']

    # LMAO. You can't have on_message and command listener :nfr:

    # set filter role
    if(args[0] == f'{prefix}filterrole'):
        if(message.author.guild_permissions.administrator == False):
            await message.channel.send('You do not have the permission to use this command!', delete_after=5)
            return
        await cmd.setfilterrole(guild, message, args)

    # filter
    elif(args[0] == f'{prefix}filter'):
        if(message.author.guild_permissions.administrator == False):
            await message.channel.send('You do not have the permission to use this command!', delete_after=5)
            return
        await cmd.filtercommand(guild, message, args)
    
    # purge
    elif(args[0] == f'{prefix}purge'):
        if(message.author.guild_permissions.administrator == False):
            await message.channel.send('You do not have the permission to use this command!', delete_after=5)
            return
        await cmd.purge(guild, message, args)

    # set cfg.config option manually
    elif(args[0] == f'{prefix}setconfig'):
        if(message.author.guild_permissions.administrator == False):
            await message.channel.send('You do not have the permission to use this command!', delete_after=5)
            return
        await cmd.setconfig(guild, message, args)
    
    elif(args[0] == f'{prefix}kick'):
        if(message.author.guild_permissions.administrator == False):
            await message.channel.send('You do not have the permission to use this command!', delete_after=5)
            return
        await cmd.kick(guild, message, args)

    elif(args[0] == f'{prefix}ban'):
        if(message.author.guild_permissions.administrator == False):
            await message.channel.send('You do not have the permission to use this command!', delete_after=5)
            return
        await cmd.ban(guild. message)

    elif(args[0] == f'{prefix}warn'):
        if(message.author.guild_permissions.administrator == False):
            await message.channel.send('You do not have the permission to use this command!', delete_after=5)
            return
        await cmd.warn(guild, message, args)

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
