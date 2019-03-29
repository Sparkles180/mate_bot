import sys

from discord.ext import commands

from cogs.base_cog import BaseCog
from utils.checks import is_admin
from utils.reload import reload_helper_func


class AdminCog(BaseCog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @is_admin()
    async def reload(self):
        await self.bot.say("reloading bot")
        await reload_helper_func(self.bot)

    @commands.command(pass_context=True)
    @is_admin()
    async def close(self):
        await self.bot.logout()
        sys.exit(-1)


def setup(bot):
    bot.add_cog(AdminCog(bot))
