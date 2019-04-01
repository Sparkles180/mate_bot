from functools import reduce
from discord.ext import commands
from cogs.base_cog import BaseCog
from utils.db import Database

db = None


class FeatureRequestCog(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(pass_context=True)
    async def request(self, ctx, *args):
        get_db()
        db.make_request(ctx.message.author.name, reduce(lambda x, y: x+" " + y, args))

    @commands.command()
    async def get_requests(self):
        get_db()
        await  self.bot.say(db.get_requests())


def get_db():
    global db
    if db is None:
        db = Database()


def setup(bot):
    get_db()
    db.create_table()
    bot.add_cog(FeatureRequestCog(bot))
