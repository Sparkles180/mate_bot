import sys


async def reload_helper_func(self):
    await self.bot.logout()
    sys.exit(0)
