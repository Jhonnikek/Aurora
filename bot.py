import discord
import os
import logging
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

class Aurora(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        activity = discord.Game(name='not being in epstein files')
        super().__init__(intents=intents, command_prefix=commands.when_mentioned_or("!"), activity=activity, help_command=None)

    async def on_ready(self):
        print(f"{self.user.name} is online")

    async def setup_hook(self) -> None:
        await self.load_extension('cogs.memes')
        return await super().setup_hook()

if __name__ == "__main__":
    bot = Aurora()
    bot.run(os.getenv("TOKEN"), log_handler=handler)