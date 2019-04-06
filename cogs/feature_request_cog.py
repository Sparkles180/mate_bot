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
            request_str = "user {} requests {}".format(request.get("user_name"), request.get("content"))
            embed.add_field(name="Request id: {}".format(request.get('id')), value=request_str, inline=False)
        await  self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command()
    async def finished(self, request_id):
        get_db()
        db.request_complete(request_id)


def get_db():
    global db
    if db is None:
        db = Database()


def setup(bot):
    get_db()
    db.create_table()
    bot.add_cog(FeatureRequestCog(bot))
