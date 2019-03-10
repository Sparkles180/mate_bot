import asyncio
import os

from discord import Game
from discord.ext.commands import Bot
from utils import checks

BOT_PREFIX = ("?", "!")
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))


@client.command()
async def play(song):
    await client.say("this will get \"{}\" from youtube".format(song))


@client.command()
@checks.is_owner()
async def _reload():
    pass


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
