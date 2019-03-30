from discord.ext import commands

from cogs.base_cog import BaseCog


class FeatureRequestCog(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command()
    async def request(self, *args):
        pass


def setup(bot):
    bot.add_cog(FeatureRequestCog(bot))