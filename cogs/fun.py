import aiohttp
from discord.ext import commands
import logging
import random


class Fun(commands.Cog):
    def __init__(self, bot) -> None:
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

    @commands.command()
    async def ping(self, ctx) -> None:
        await ctx.send("pong!")

    @commands.command()
    async def roll(self, ctx, sides: int = 6) -> None:
        """Rolls a die with a specified number of sides."""
        result = random.randint(1, sides)
        await ctx.send(f"{result} 🎲")


async def setup(bot):
    await bot.add_cog(Fun(bot))
