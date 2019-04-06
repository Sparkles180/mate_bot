from functools import reduce

import discord
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

    @commands.command(pass_context=True)
    async def get_requests(self, ctx):
        get_db()
        embed = discord.Embed(title='Requests')
        for request in db.get_requests():
            embed.add_field(name=request.get("user_name"), value=request.get("content"), inline=False)
        await  self.bot.send_message(ctx.message.channel, embed=embed)


def get_db():
    global db
    if db is None:
        db = Database()


def setup(bot):
    get_db()
    db.create_table()
    bot.add_cog(FeatureRequestCog(bot))
