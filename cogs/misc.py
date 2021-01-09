#!/usr/bin/env python3
# misc.py
# random assorted commands that don't fit into any category
import discord, cfg, owouwu, filtercheck, random, json
from urllib.request import Request, urlopen
from  discord.ext import commands
from context import messagecontext

api_url = 'https://nekos.life/api/v2/img/neko'

swf_leo_urls = [
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__8e96e4a2ccca4c473bd683787b306296.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__86e896a8c3c9de96c8b31fc091e08f44.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__b49d6e7bed35959ed9e3cd1983bf7c90.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__fda65fadffcd52376770f1867ad79dfb.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__2a5ee9d76eddc635b3c3c5785dff896f.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__f188c82d662f212b7365617819721eb2.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__6c45b64e0877c45cd29d0a71196e0b9d.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__7251dc37089a374abd698fd752f0c321.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__6e68a9e756d4315fe584203e7886afab.jpg',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__4b2b092943c1d0e8404aefe38a880197.jpg',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__3a8f275383204f966999d0b7c6fab38e.jpg',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__c8ad4f0e75e97dfc565902a61c6a1320.jpg',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__dc1c40ea7911e30037281fe607e1e1fb.jpg',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__76a7f201c9d599dbedd86586d17e2c6a.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__7231c0258aa74aac74074c7932379101.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__be8f9c9a811004d1865155ce66f196af.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__b984e75d3e635855ead542a49771568a.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__20b1ba4ad58945dac2993183c2191a76.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__fc0fec86761ab31f58e5d9490eae1aae.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_nijihashi_sora__40c355221b9a8799e3dd587b381154fc.jpg',
    'https://cdn.donmai.us/original/3d/02/__leo_original_drawn_by_mafuyu_chibi21__3d0242486d220be8463946cda2f47daa.png',
    'https://cdn.donmai.us/original/77/6b/__leo_original_drawn_by_mafuyu_chibi21__776be21dab2dac7b2e58832bfcada747.png',
    'https://cdn.donmai.us/original/3c/4f/__leo_original_drawn_by_mafuyu_chibi21__3c4ffbb99fda42f0cb0bd8a5a8407298.jpg',
    'https://cdn.donmai.us/original/59/2b/__leo_original_drawn_by_mafuyu_chibi21__592b5310adf37ed3e212243ca565b464.png'
    ]

nsfw_leo_urls = [
    'https://cdn.donmai.us/original/16/ce/__leo_original_drawn_by_mafuyu_chibi21__16cec9763c47fd306bc0ca41647ad017.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__02e709b6dac56211111ba38d78142ce2.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__0b082db94f59ceb7a300ade32e89b8c4.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__b09199ab4c8c2794ada13bc1fef2d1ce.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__60c0ee117674880e7cfbf25e9ab0aec4.png',
    'https://danbooru.donmai.us/data/__leo_original_drawn_by_mafuyu_chibi21__ff139dedc4429cdaf7327ba33f060432.png'
]

class Misc(commands.Cog):
    """Misc"""

    def __init__(self, bot):
        self.bot = bot
        print('Cog "Misc" loaded')

    @commands.command(name='hello', hidden=True)
    @commands.is_owner()
    async def hello_command(self, ctx):
        """UwU"""

        await ctx.send(f'Hello master! {owouwu.gen()}')
        
    @commands.check(cfg.isguild)
    @commands.command(name='say', aliases=['copy', 'mimic'])
    async def say_command(self, ctx, *, message: str):
        """Makes me say what you tell me to!"""

        if '@' in message and '<' in message and '>' in message or '@everyone' in message or '@here' in message:
            await ctx.send('I cannot mention users!', delete_after=5)
            return

        if await filtercheck.breaks_filter(messagecontext(ctx.message)):
            return

        await ctx.send(message)

    @commands.check(cfg.isguild)
    @commands.check(cfg.hasperms)
    @commands.command(name='sayembed')
    async def send_embed(self, ctx, title: str, *content: str):
        """Sends a embed with the given title and content. Intended for use by moderators in the rules channel."""

        if not title:
            await ctx.send('Usage: sayembed title content', delete_after=5)

        if not content:
            await ctx.send('Usage: sayembed title content', delete_after=5)

        # turn content from a list into a string
        desc = ' '.join(content)

        embed = discord.Embed(description=desc, title=title, colour=0xFB98FB)

        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='stopbot', hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shutdown"""

        # log botevent
        botevent_log = f'logs/botevent/botevent.log'
        message = f'{str(datetime.now())} Shutting down!\n'
        write_log_message(message, botevent_log)

        await ctx.send(f'Going to sleep! {owouwu.gen()}')
        sys.exit()

    @commands.command(name='status', hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx, *, status: str="catgirls"):
        """Sets bot status"""

        await cfg.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

# add cog
def setup(bot):
    bot.add_cog(Misc(bot))
