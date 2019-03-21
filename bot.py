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
        self.players = {}
        self.queues = {}

        for extension in startup_extension:
            self.load_extension(extension)

        async def on_ready(self):
            await client.change_presence(game=Game(name="with humans"))
            print("Logged in as " + client.user.name)

        async def on_message(self, message):
            if message.server.id == "554431614042636317" and \
                    str(message.author) == "GitHub#0000":
                await client.send_message(message.channel, "reloading mate")
                await reload_helper_func()
            await client.process_commands(message)

        @commands.command(pass_context=True)
        async def test(self, ctx):
            await self.bot.say("test")


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

client = MateBot()

client.run(TOKEN)
