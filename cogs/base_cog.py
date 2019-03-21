class BaseCog(object):
    def __init__(self, bot):
        self.bot = bot

    async def leave(self, ctx):
        server = ctx.message.server
        if self.bot.is_voice_connected(server):
            voice_client = self.bot.voice_client_in(server)
            await voice_client.disconnect()

    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        if not channel:
            await self.bot.say("join a server nerd")
            return None
        if not self.bot.is_voice_connected(channel.server):
            return await self.bot.join_voice_channel(channel)
        return None

