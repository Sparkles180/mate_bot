import asyncio
import os

from discord import Game
from discord.ext.commands import Bot
import youtube_dl

BOT_PREFIX = ("?", "!")
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

client = Bot(command_prefix=BOT_PREFIX)

players = {}


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))


@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()


@client.command(pass_context=True)
async def stop(ctx):
    server = ctx.message.server
    players.get(server.id).stop()


@client.command(pass_context=True)
async def pause(ctx):
    server = ctx.message.server
    players.get(server.id).pause()


@client.command(pass_context=True)
async def resume(ctx):
    server = ctx.message.server
    player = players.get(server.id).resume()


@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)

"""
!play https://www.youtube.com/watch?v=pfCYPVxWEMI
"""