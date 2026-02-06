import discord
import requests
import json
import os
import logging
from dotenv import load_dotenv

load_dotenv()

TOKE_KEY = os.getenv('TOKEN')
DEBUG = os.getenv('DEBUG') == 'True'

def get_meme():
    response = requests.get('https://meme-api.com/gimme')
    json_data = json.loads(response.text)
    return json_data['url']

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!m'):
            await message.channel.send(get_meme())

intents = discord.Intents.default()
intents.message_content = True

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

client = MyClient(intents=intents)
client.run(TOKE_KEY, log_handler=handler)
