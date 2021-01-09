#!/usr/bin/env python3
# logger.py
# log stuff to files
from context import messagecontext
from filemanager import make_dir_if_needed
import os, settings, discord, cfg

async def loggingEnabled(message) -> bool:
    return settings.get_boolean_value(message.channel.guild.id, 'loggingEnabled', True)

def write_log_message(message, path):
    # open file and write 
    try:
        f = open(path, 'a')
        f.write(message)
        f.close
    except:
        pass

async def send_discord_log_message(messagecontext, log_dict, title):

    if messagecontext.author() == cfg.bot.user:
        return

    guild_id = messagecontext.guild_id()
    pfp_url = messagecontext.author().avatar_url

    channel_id = settings.get_integer_value(guild_id, 'logchannel')
    channel = messagecontext.guild().get_channel(channel_id)

    embed_wrapper = discord.Embed(colour=0xFB98FB)
    embed_wrapper.set_author(name=title,
                        url='https://github.com/Burrit0z/catgirl-bot',
                        icon_url=pfp_url)
    
    for key in log_dict.keys():
        embed_wrapper.add_field(name=key, value=log_dict[key], inline=False)


    try:
        await channel.send(embed=embed_wrapper)
    except:
        pass

# define log function
async def logChatMessage(messagecontext):

    # write message to a file if the option is on
    enabled = await loggingEnabled(messagecontext.message)
    channel = messagecontext.channel()
    guild = messagecontext.guild()

    if enabled:

        section_folder = f'logs/guilds/{guild.id}/{channel.category.id}'
        make_dir_if_needed(section_folder)
        log_path = f'{section_folder}/{channel.id}.log'

        try:
            log_message = f'{messagecontext.readable_log()}\n'
            write_log_message(log_message, log_path)
        except:
            log_message = f'{messagecontext.log_header()}: Unable to log contents, exception occured\n'
            write_log_message(log_message, log_path)

async def logCommandSent(messagecontext):
    # log to the command log of the guild
    enabled = await loggingEnabled(messagecontext.message)
    guild = messagecontext.guild()

    log_path = f'logs/guilds/{guild.id}/commands.log'

    if enabled:
        log_message = f'{messagecontext.readable_log()}\n'
        write_log_message(log_message, log_path)

async def logMessagedAltered(oldmessage, newmessage):
    # args should be of type message context

    enabled = await loggingEnabled(oldmessage.message)
    if not enabled:
        return

    if oldmessage.message.content == newmessage.message.content:
        return

    guild = oldmessage.guild()
    log_message = f'{oldmessage.log_header()} edited message.\nOld: {oldmessage.message.content}\nNew: {newmessage.message.content}\n\n'
    log_path = f'logs/guilds/{guild.id}/messages_changed.log'

    discord_message = {
        'Author' : oldmessage.readable_author(),
        'Old message' : oldmessage.message.content,
        'New message' : newmessage.message.content
    }

    write_log_message(log_message, log_path)
    await send_discord_log_message(oldmessage, discord_message, 'Edited message')

async def logMessagedDeleted(messagecontext):
    # args should be of type message context

    enabled = await loggingEnabled(messagecontext.message)
    if not enabled:
        return

    guild = messagecontext.guild()
    log_message = f'{messagecontext.log_header()} deleted message: {messagecontext.message.content}\n\n'
    log_path = f'logs/guilds/{guild.id}/messages_changed.log'

    discord_message = {
        'Author' : messagecontext.readable_author(),
        'Message' : messagecontext.message.content
    }


    write_log_message(log_message, log_path)
    await send_discord_log_message(messagecontext, discord_message, 'Deleted Message')
