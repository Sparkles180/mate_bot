import imdb
from discord.ext import commands

from cogs.base_cog import BaseCog


class ImdbCog(BaseCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.bot = bot
        self.im = imdb.IMDb()

    @commands.command()
    async def search_movie(self, query):
        result = ""
        for movie in self.im.search_movie(query):
            result += movie['title'] + " "
        await  self.bot.say(result)


def setup(bot):
    bot.add_cog(ImdbCog(bot))

