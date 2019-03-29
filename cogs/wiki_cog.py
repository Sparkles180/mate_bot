from discord.ext import commands
import wikipedia
from cogs.base_cog import BaseCog


class Wiki(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command()
    async def wiki(self, query):
        wi = wikipedia.page(query)
        await self.bot.say(wi.url)

def setup(bot):
    bot.add_cog(Wiki(bot))
