# mate bot

This is a general purpose bot that I made because I was bored.

## development
To add new commands, create a new class in cogs that extends the base cog.
Make sure to make the file *_cog.py and it will be loaded on start.
For example:
make a file cogs/my_cog.py
```
class MyCog(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)

    @commands.command()
    async def hello(self):
        await self.bot.say("hello")


def setup(bot):
    bot.add_cog(MyCog(bot))
```

in order to run locally you need a discord token and youtube api key

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```

## deployment

When changes are pushed master the bot will reload and pull the latest version from git.