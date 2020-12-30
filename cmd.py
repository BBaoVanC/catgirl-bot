#!/usr/bin/env python3

import json


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

async def purge(guild, message, args):
    if(len(args) != 2):
        await message.channel.send(f'Usage: purge number', delete_after=5)
        return
    messages = await message.channel.purge(limit=int(args[1]))
    await message.channel.send(f'Deleted {len(messages)} message(s)', delete_after=5)
