import requests
import json
from discord.ext import commands

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        response = requests.get('https://meme-api.com/gimme')
        meme_data = response.json()
        await ctx.send(meme_data['url'])

async def setup(bot):
    await bot.add_cog(Memes(bot))
