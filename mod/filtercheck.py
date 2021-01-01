from context import messagecontext
import cfg, json, owouwu

# define message check function
# checks against filter and some other things
async def checkMessage(messagecontext):

    # split message into an array to check individual words
    words = messagecontext.message_words()
    message = messagecontext.message
    lowered_content = message.content.lower()
    
    # react to these terms
    if 'catgirl' in lowered_content or 'neko' in lowered_content or 'sex' in lowered_content:
        await message.add_reaction('<:wooaaahhh:789297106837569557>') #wooaaahhh
    
    # pedo. search for individual words
    if ('cp' in words) or ('child' in words and 'porn' in words):
        try:
            await messagecontext.message.delete()
            await messagecontext.message.author.kick()
            await messagecontext.channel().send(f'{message.author.name} has been kicked for being a literal pedo')
        except:
            print(f'Error kicking user {message.author.name} from {messagecontext.guild().name}! Does bot have correct permissions to kick this user?')

    # gm gn reacts
    if 'gm' in words or 'gn' in words:
        if 'gm' in words:
            await message.add_reaction('<:catgm:782652523462393918>')
        if 'gn' in words:
            await message.add_reaction('<:catgn:782652492847775794>')
    
    if 'i love you' in lowered_content:
        await message.add_reaction('<:love:794076402945228811>')

    if cfg.bot.user in message.mentions:
        await message.channel.send(owouwu.gen())

    # check filters
    # exempt users with no filter role
    try:
        if messagecontext.guild().get_role(cfg.config.getint(f'{messagecontext.guild_id()}', 'filterrole')) in message.author.roles:
            return
    except:
        await messagecontext.channel().send('No filter role is not set! Please set nofilter role with filterrole command!')

    # cursed code to load filter as a list and check the message
    filter_str = cfg.config[f'{messagecontext.guild_id()}']['filter']
    filter_list = json.loads(filter_str) # loads as list
    if messagecontext.contains_filtered_terms(filter_list):
        await messagecontext.channel().send(content=f'{message.author.mention}, that word is not allowed here!', delete_after=10)
        try:
            await messagecontext.message.delete()
        except:
            print(f'Failed to delete message in guild {messagecontext.guild().name}')
