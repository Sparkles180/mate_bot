from discord.ext import commands

from cogs.base_cog import BaseCog
from utils.search import search


class Music(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.players = {}
        self.queues = {}

    @commands.command(pass_context=True)
    async def play(self, ctx, song):
        await self.join(ctx)
        server = ctx.message.server
        voice_client = self.bot.voice_client_in(server)
        player = await voice_client.create_ytdl_player(search(song), after=lambda: self.check_queue(ctx))
        if self.players.get(server.id) is None:
            self.players[server.id] = player
            player.start()
            await  self.bot.say("now playing " + player.title)
        else:
            await self.queue(server.id, player)

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        server = ctx.message.server
        if not self.players.get(server.id) is None:
            self.players.get(server.id).stop()
            self.players.pop(server.id)
        await self.leave(ctx)

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        server = ctx.message.server
        self.players.get(server.id).pause()

    @commands.command(pass_context=True)
    async def resume(self, ctx):
        server = ctx.message.server
        self.players.get(server.id).resume()

    @commands.command(pass_context=True)
    async def skip(self, ctx):
        server = ctx.message.server
        if len(self.queues) <= 1:
            self.players.get(server.id).stop()
        else:
            await self.bot.say("Last song mate")

    @commands.command(pass_context=True)
    async def m8(self, ctx):
        server = ctx.message.server
        voice_channel = await self.join(ctx)
        if not voice_channel:
            return None
        player = voice_channel.create_ffmpeg_player('M8.mp4', after=lambda: self.check_queue(ctx))
        self.players[server.id] = player
        player.start()

    @commands.command(pass_context=True)
    async def list_playlist(self, ctx):
        server = ctx.message.server
        result = []
        for player in self.queues[server.id]:
            result += [player.title]
        await self.bot.say("queued videos are " + str(result))

    async def queue(self, server_id, player):
        if server_id in self.queues:
            self.queues[server_id].append(player)
        else:
            self.queues[server_id] = [player]
        await self.bot.say("video queue " + player.title)

    def check_queue(self, ctx):
        server_id = ctx.message.server.id;
        if self.queues[server_id]:
            self.players[server_id] = self.queues[server_id].pop(0)
            self.players[server_id].start()
            self.bot.say("now playing: " + self.players[server_id].title)
        elif not self.queues[server_id]:
            self.leave(ctx)


def setup(bot):
    bot.add_cog(Music(bot))
