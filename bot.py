import asyncio
import os
import subprocess

from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot

from utils import checks
from utils.checks import is_admin

BOT_PREFIX = "$"
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
    await leave(ctx)


@client.command(pass_context=True)
async def pause(ctx):
    server = ctx.message.server
    players.get(server.id).pause()


@client.command(pass_context=True)
async def resume(ctx):
    server = ctx.message.server
    players.get(server.id).resume()


async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    if channel is None:
        client.say("join a server nerd")
        return None
    if not client.is_voice_connected(channel.server):
        return await client.join_voice_channel(channel)
    return None


async def leave(ctx):
    server = ctx.message.server
    if client.is_voice_connected(server):
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()


@client.command(pass_context=True)
async def m8(ctx):
    server = ctx.message.server
    voice_channel = await join(ctx)
    if voice_channel is None:
        voice_channel = client.voice_client_in(server)
    player = voice_channel.create_ffmpeg_player('M8.mp4', after=lambda: print('done'))
    players[server.id] = player
    player.start()


@client.command(pass_context=True)
@is_admin()
async def reload():
    await client.logout()
    subprocess.Popen(['bash', '-c', '. manager.sh; reload'])


@client.command(pass_context=True)
@is_admin()
async def close():
    await client.logout()


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
