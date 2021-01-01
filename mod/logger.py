from context import messagecontext
import os, settings

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
    message = messagecontext.message
    channel = messagecontext.channel()
    guild = messagecontext.guild()

    if enabled:

        section_folder = f'logs/guilds/{guild.id}/{channel.category.id}'
        settings.make_dir_if_needed(section_folder)
        log_path = f'{section_folder}/{channel.id}'

        try:
            message = f'{messagecontext.readable_log()}\n'
            write_log_message(message, log_path)
        except:
            message = f'{messagecontext.log_header()}: Unable to log contents, exception occured\n'
            write_log_message(message, log_path)
