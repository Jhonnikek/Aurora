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
        activity = discord.Game(name="Not in epstein files")
        status = discord.Status.do_not_disturb
        super().__init__(
            intents=intents,
            command_prefix=commands.when_mentioned_or("!"),
            activity=activity,
            status=status,
            help_command=None,
        )

    async def on_ready(self):
        print(f"{self.user.name} is online")

    async def load_cogs(self) -> None:
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                extension = file.rstrip(".py")
                await self.load_extension(f"cogs.{extension}")

    async def setup_hook(self) -> None:
        await self.load_cogs()
        return await super().setup_hook()


if __name__ == "__main__":
    bot = Aurora()
    bot.run(os.getenv("TOKEN"), log_handler=handler)
