from context import messagecontext
import os, cfg

async def loggingEnabled(message) -> bool:
    enabled = True
    try:
        enabled = cfg.config.getboolean(str(message.channel.guild.id), 'loggingEnabled')
    except:
        await message.channel.send('Warning: Could not convert the value of "loggingEnabled" to a boolean, defaulting to True.\nPlease make sure you have set yes or no for this option')

    return enabled

# define log function
async def logChatMessage(messagecontext):

    # write message to a file if the option is on
    enabled = await loggingEnabled(messagecontext.message)
    message = messagecontext.message
    channel = messagecontext.channel()
    guild = messagecontext.guild()

    if enabled:
        try:

            # open file and write 
            f = open(f'logs/guilds/{guild.id}/{channel.name}.log', 'a')
            f.write(messagecontext.readable_log())
            f.close
        except:
            f = open(f'logs/guilds/{guild.id}/{channel.name}.log', 'a')
            f.write(f'{messagecontext.log_header()}: Unable to log contents, exception occured\n')
            f.close