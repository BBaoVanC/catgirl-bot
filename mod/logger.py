#!/usr/bin/env python3
# logger.py
# log stuff to files
from context import messagecontext
from filemanager import make_dir_if_needed
import os

async def loggingEnabled(message) -> bool:
    enabled = True
    try:
        enabled = get_boolean_value(message.channel.guild.id, 'loggingEnabled')
    except:
        pass

    return enabled

def write_log_message(message, path):
    # open file and write 
    f = open(path, 'a')
    f.write(message)
    f.close

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

    if oldmessage.message.content == newmessage.message.content:
        return

    guild = oldmessage.guild()
    log_message = f'{oldmessage.log_header()} altered message.\nOld: {oldmessage.message.content}\nNew: {newmessage.message.content}\n\n'
    log_path = f'logs/guilds/{guild.id}/messages_changed.log'

    write_log_message(log_message, log_path)

async def logMessagedDeleted(messagecontext):
    # args should be of type message context
    guild = messagecontext.guild()
    log_message = f'{messagecontext.log_header()} deleted message: {messagecontext.message.content}\n\n'
    log_path = f'logs/guilds/{guild.id}/messages_changed.log'

    write_log_message(log_message, log_path)
