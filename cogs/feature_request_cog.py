from functools import reduce
import mysql.connector
from discord.ext import commands
from cogs.base_cog import BaseCog
from mate_config import config


class FeatureRequestCog(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command(pass_context=True)
    async def request(self, ctx, *args):
        connection = get_connection()
        cursor = connection.cursor()
        sql_query = "INSERT INTO requests (user_name, content) VALUES (%s, %s);"
        cursor.execute(sql_query, (ctx.message.author.name, reduce(lambda x, y: x+" " + y, args)))
        connection.commit()
        cursor.close()
        connection.close()


def get_connection():
    return mysql.connector.connect(
        host="remotemysql.com",
        user="2OPrqL0Qb3",
        passwd=config.get("mysql_password"),
        database="2OPrqL0Qb3"
    )


def setup(bot):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests(
             id INT auto_increment,
            user_name varchar(255) NOT NULL ,
            content TEXT,
            PRIMARY KEY (id)
        );
        """)
    cursor.close()
    connection.close()
    bot.add_cog(FeatureRequestCog(bot))
