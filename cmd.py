#!/usr/bin/env python3

import json

import cfg


# commands
async def kick(guild, message, args):
    reason = "No reason"
    if(len(args) < 2):
        await message.channel.send(f'Usage: kick user reason (optional)', delete_after=5)
        return
    elif(len(args) >= 3):
        del args[0]
        del args[0]
        reason = ' '.join(args)

    members = message.mentions
    for mem in members:
        await mem.send(f'You have been kicked from {guild.name} for reason: {reason}')
        await guild.kick(mem)
    
    await message.channel.send(f'Members kicked', delete_after=5)
    await message.add_reaction('✅')

async def ban (guild, message, args):
    reason = "No reason"
    if(len(args) < 2):
        await message.channel.send(f'Usage: ban user reason (optional)', delete_after=5)
        return
    elif(len(args) >= 3):
        del args[0]
        del args[0]
        reason = ' '.join(args)

    members = message.mentions
    for mem in members:
        await mem.send(f'You have been banned from {guild.name} for reason: {reason}')
        await guild.ban(mem)

    await message.channel.send(f'Members banned', delete_after=5)
    await message.add_reaction('✅')

async def warn(guild, message, args):
    reason = "No reason"
    if(len(args) < 2):
        await message.channel.send(f'Usage: warn user reason (optional)', delete_after=5)
        return
    elif(len(args) >= 3):
        del args[0]
        del args[0]
        reason = ' '.join(args)

    members = message.mentions
    for mem in members:
        await mem.send(f'You have been warned from the moderators of {guild.name} for reason: {reason}. \n\nIf you continue to break the rules, you may be kicked or banned.')
    
    await message.channel.send(f'Members warned', delete_after=5)
    await message.add_reaction('✅')

async def setconfig(guild, message, args):
    if(len(args) != 3):
        await message.channel.send(f'Usage: setconfig option value', delete_after=5)
        return

    try:
        cfg.config['SERVER'][args[1]] = args[2]
        file = open('config/bot/settings', 'w')
        cfg.config.write(file)
        file.close()
        await message.channel.send(f'Set option {args[1]} to {args[2]}', delete_after=5)
        await message.add_reaction('✅')
    except:
        await message.channel.send(f'Command failed to execute', delete_after=5)

async def purge(guild, message, args):
    if(len(args) != 2):
        await message.channel.send(f'Usage: purge number', delete_after=5)
        return
    messages = await message.channel.purge(limit=int(args[1]))
    await message.channel.send(f'Deleted {len(messages)} message(s)', delete_after=5)

async def filtercommand(guild, message, args):
    if(len(args) != 3):
        await message.channel.send(f'Usage: filter add/remove word', delete_after=5)
        return
    
    filter = json.loads(cfg.config['SERVER']['filter'])
    if(args[1] == 'add'):
        filter.append(args[2])
    elif(args[1] == 'remove'):
        filter.remove(args[2])
    else:
        await message.channel.send(f'Usage: filter add/remove word', delete_after=5)
        return

    # save the file, convert the ' to " first, since json dies
    cfg.config['SERVER']['filter'] = f'{filter}'.replace('\'','"')

    try:
        file = open('config/bot/settings', 'w')
        cfg.config.write(file)
        file.close()
        if(args[1] == 'add'):
            await message.channel.send(f'Word {args[2]} added to filter', delete_after=5)
        elif(args[1] == 'remove'):
            await message.channel.send(f'Word {args[2]} removed from filter', delete_after=5)
        
        await message.add_reaction('✅')
    except:
        await message.channel.send(f'Command failed to execute', delete_after=5)

async def setfilterrole(guild, message, args):
    if(len(args) != 2):
        await message.channel.send(f'Usage: filterrole role_id', delete_after=5)
        return
    print(f'No filter role set to {guild.get_role(int(args[1]))}')
    await message.channel.send(f'No filter role set to "{guild.get_role(int(args[1]))}"', delete_after=5)
    await message.add_reaction('✅')

    # save file
    cfg.config['SERVER']['filterrole'] = args[1]
    try:
        file = open('config/bot/settings', 'w')
        cfg.config.write(file)
        file.close()
    except:
        await message.channel.send(f'Command failed to execute', delete_after=5)