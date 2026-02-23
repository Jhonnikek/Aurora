from __future__ import annotations
from discord.ext import commands
import random


class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

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
