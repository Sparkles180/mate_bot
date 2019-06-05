import sys


async def reload_helper_func(bot):
    await bot.logout()
    sys.exit(0)
