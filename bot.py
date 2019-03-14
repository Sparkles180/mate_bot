import asyncio
import os
import subprocess
import sys

import discord
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot

from utils.checks import is_admin

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

client = Bot(command_prefix=commands.when_mentioned_or("$"))

players = {}
queues = {}


def check_queue(server_id):
    if queues[server_id]:
        player = queues[server_id].pop(0)
        player.start()
        client.say("now playing: " + player.title)


async def queue(server_id, player):
    if server_id in queues:
        queues[server_id].append(player)
    else:
        queues[server_id] = [player]
    await client.say("video queue " + player.title)


async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    if not channel:
        await client.say("join a server nerd")
        return None
    if not client.is_voice_connected(channel.server):
        return await client.join_voice_channel(channel)
    return None


async def leave(ctx):
    server = ctx.message.server
    if client.is_voice_connected(server):
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()


async def reload_helper_func():
    await client.logout()
    sys.exit(0)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.command(pass_context=True)
async def test(ctx):
    await client.say("test")


"""Music Commands"""


@client.command(pass_context=True)
async def play(ctx, url):
    await join(ctx)
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    if players.get(server.id) is None:
        players[server.id] = player
        player.start()
        await  client.say("now playing " + player.title)
    else:
        await queue(server.id, player)


@client.command(pass_context=True)
async def stop(ctx):
    server = ctx.message.server
    players.get(server.id).stop()
    players.pop(server.id)
    await leave(ctx)


@client.command(pass_context=True)
async def pause(ctx):
    server = ctx.message.server
    players.get(server.id).pause()


@client.command(pass_context=True)
async def resume(ctx):
    server = ctx.message.server
    players.get(server.id).resume()


@client.command(pass_context=True)
async def skip(ctx):
    server = ctx.message.server
    if len(queues) <= 1:
        players.get(server.id).stop()
    else:
        await client.say("Last song mate")


@client.command(pass_context=True)
async def m8(ctx):
    server = ctx.message.server
    voice_channel = await join(ctx)
    if not voice_channel:
        return None
    player = voice_channel.create_ffmpeg_player('M8.mp4', after=lambda: print('done'))
    players[server.id] = player
    player.start()


@client.command(pass_context=True)
async def list_playlist(ctx):
    server = ctx.message.server
    result = []
    for player in queues[server.id]:
        result += [player.title]
    await client.say("queued videos are " + str(result))


"""admin commands"""


@client.command(pass_context=True)
@is_admin()
async def reload():
    await reload_helper_func()


@client.command(pass_context=True)
@is_admin()
async def close():
    await client.logout()
    sys.exit(-1)


@client.event
async def on_message(message):
    if message.server.id == "554431614042636317" and \
            str(message.author) == "GitHub#0000":
        await client.send_message(message.channel, "reloading mate")
        await reload_helper_func()
    await client.process_commands(message)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.run(TOKEN)
