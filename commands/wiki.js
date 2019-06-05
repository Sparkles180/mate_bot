const wiki = require('wikijs').default;

module.exports = {
    name: 'wiki',
    args: true,
    description: 'Information about the arguments provided.',
    execute(message, args) {
        wiki().search(args, 1)
            .then( data => wiki().page(data.results[0]))
            .then( page => message.reply(page.raw.fullurl));
    },
};

// from discord.ext import commands
// import wikipedia
// from cogs.base_cog import BaseCog
//
//
// class Wiki(BaseCog):
//     def __init__(self, bot):
//     super().__init__(bot)
//
// @commands.command()
// async def wiki(self, *args):
//     # todo add page check error
//     query = ""
//     for item in args:
//     query += item
//     wi = wikipedia.page(query)
//     await self.bot.say(wi.url)
//
//
// def setup(bot):
//     bot.add_cog(Wiki(bot))
