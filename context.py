from discord.ext import commands


class Context(commands.Context):
    async def sendstr(self, strname, *args, delete_after=None, **kwargs):
        return await self.send(
            self.bot.getstr(self.author, strname).format(*args, **kwargs),
            delete_after=delete_after,
        )
