#!/usr/bin/env python3
# filtercheck.py
# function to check message content
from context import messagecontext
import cfg, settings, json, owouwu

# define message check function
# checks against filter and some other things
async def checkMessage(messagecontext):

    # split message into an array to check individual words
    words = messagecontext.message_words()
    message = messagecontext.message
    lowered_content = message.content.lower()

    # reactions
    if settings.get_boolean_value(messagecontext.guild_id(), 'reactions', True):
    
        # react to these terms
        if 'catgirl' in lowered_content or 'neko' in lowered_content or 'sex' in lowered_content:
            await message.add_reaction('<:wooaaahhh:789297106837569557>') #wooaaahhh

        # gm gn reacts
        if 'gm' in words or 'gn' in words:
            if 'gm' in words:
                await message.add_reaction('<:catgm:782652523462393918>')
            if 'gn' in words:
                await message.add_reaction('<:catgn:782652492847775794>')
        
        if 'i love you' in lowered_content:
            await message.add_reaction('<:love:794076402945228811>')

    # respond to pings
    if cfg.bot.user in message.mentions:
        await message.channel.send(owouwu.gen())

    # check filters
    # exempt users with no filter role
    if messagecontext.guild().get_role(settings.get_integer_value(messagecontext.guild_id(), 'filterrole')) in message.author.roles:
        return

    filtered = await breaks_filter(messagecontext)
    if filtered:
        await messagecontext.channel().send(content=f'{message.author.mention}, that word is not allowed here!', delete_after=10)
        try:
            await messagecontext.message.delete()
        except:
            print(f'Failed to delete message in guild {messagecontext.guild().name}')


async def breaks_filter(messagecontext) -> bool:
    message = messagecontext.message

    filter_str = settings.get_value(messagecontext.guild_id(), 'filter')
    filter_list = json.loads(filter_str) # loads as list
    if messagecontext.contains_filtered_terms(filter_list):
        return True

    return False
