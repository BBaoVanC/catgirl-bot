from context import messagecontext
import cfg, json

# define message check function
# checks against filter and some other things
async def checkMessage(messagecontext):

    # split message into an array to check individual words
    words = messagecontext.message_words()
    message = messagecontext.message
    
    # react
    if 'catgirl' in words or 'neko' in words or 'sex' in words:
        await message.add_reaction('<:wooaaahhh:789297106837569557>') #wooaaahhh
    
    # pedo
    elif ('cp' in words) or ('child' in words and 'porn' in words):
        try:
            await messagecontext.message.delete()
            await messagecontext.message.author.kick()
            await messagecontext.channel().send(f'{message.author.name} has been kicked for being a literal pedo')
        except:
            print(f'Error kicking user {message.author.name} from {messagecontext.guild().name}! Does bot have correct permissions to kick this user?')
   
    # check filters
    else:
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