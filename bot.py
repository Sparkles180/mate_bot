import asyncio
import os
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from utils.reload import reload_helper_func

startup_extension = ['cogs.music','cogs.admin', 'cogs.imdb_cog']


class MateBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("$"), case_insenitive=True)

        for extension in startup_extension:
            self.load_extension(extension)


TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

client = MateBot()


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.event
async def on_message(message):
    if message.server.id == "554431614042636317" and \
            str(message.author) == "GitHub#0000":
        await client.send_message(message.channel, "reloading mate")
        await reload_helper_func(client)
    await client.process_commands(message)

client.run(TOKEN, reconnect=True)
