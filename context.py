from discord.ext import commands

class Context(commands.Context):
    def getstr(self, strname):
        uconf = self.bot.uconf.get(self.author.id)
        lang = uconf['language'] if uconf else 'en'
        text = self.bot.strings[lang][strname]
        return text

    async def sendstr(self, strname, delete_after=None, *args, **kwargs):
        return await self.send(self.getstr(strname).format(*args, **kwargs),
            delete_after=delete_after)