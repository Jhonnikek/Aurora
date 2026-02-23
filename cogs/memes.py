import aiohttp
from discord.ext import commands
import logging


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        await self.session.close()

    @commands.command()
    async def meme(self, ctx):
        try:
            async with self.session.get("https://meme-api.com/gimme") as response:
                if response.status == 200:
                    meme_data = await response.json()
                    await ctx.send(meme_data["url"])
                else:
                    logging.warning(
                        f"Meme API request failed with status: {response.status}"
                    )
        except aiohttp.ClientError as e:
            logging.error(f"Error fetching meme: {e}")


async def setup(bot):
    await bot.add_cog(Memes(bot))
