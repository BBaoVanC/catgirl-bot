#!/usr/bin/env python3
# image.py
# image-based commands
import discord, cfg, owouwu, random, json
from cooldown import cooldown
from urllib.request import Request, urlopen
from discord.ext import commands

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

class Image(commands.Cog):
    """Image"""

    def __init__(self, bot):
        self.bot = bot
        self.cooldown = cooldown(2)
        print('Cog "Image" loaded')

    @commands.check(cfg.isguild)
    @commands.command(name='jumbo', aliases=['emote'])
    async def enlarge_emote(self, ctx, emote: discord.PartialEmoji):
        """Large emote"""
        # inspired by gir's jumbo command

        embed = discord.Embed(colour=0xFB98FB)
        embed.set_image(url=emote.url)
        embed.set_footer(text=f'Requested by {ctx.message.author.name}')
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.check(cfg.isguild)
    @commands.command(name='leo')
    async def random_leo(self, ctx, *, option: str='s'):
        """Sends a random Leo pic, may or may not be lewd"""

        if not await self.cooldown.check_and_warn_usage(ctx.channel):
            return
        self.cooldown.was_used(ctx.guild.id)

        if not option:
            await ctx.send('Error: please specify an option, either s (sfw) or n (nsfw)', delete_after=5)
            return

        if option == 's':
            leo_url = random.choice(swf_leo_urls)
        elif option == 'n':
            if not ctx.channel.is_nsfw():
                await ctx.send('Error: the NSFW option may only be used in NSFW channels!', delete_after=5)
                return
            leo_url = random.choice(nsfw_leo_urls)
        else:
            await ctx.send('Error: please specify an option, either s (sfw) or n (nsfw)', delete_after=5)
            return

        embed = discord.Embed(title='Random Leo pic', colour=0xFB98FB)
        embed.set_image(url=leo_url)
        embed.set_footer(text=f'Requested by {ctx.message.author.name}')
        await ctx.send(content=f'Here you go {owouwu.gen()}', embed=embed)

    @commands.check(cfg.isguild)
    @commands.command(name='neko')
    async def random_neko(self, ctx):
        """Sends a random neko pic"""

        if not await self.cooldown.check_and_warn_usage(ctx.channel):
            return
        self.cooldown.was_used(ctx.guild.id)

        headers = {'User-Agent': 'Mozilla/5.0'}
        request = Request(api_url, headers=headers)
        url_content = urlopen(request).read()
        image_url = json.loads(url_content)['url']

        embed = discord.Embed(title='Random neko pic', colour=0xFB98FB)
        embed.set_image(url=image_url)
        embed.set_footer(text=f'Requested by {ctx.message.author.name}')
        await ctx.send(content=f'Here you go {owouwu.gen()}', embed=embed)

# add cog
def setup(bot):
    bot.add_cog(Image(bot))
