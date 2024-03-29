import os
import json

from discord.ext import commands
from context import Context


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uconf = {
            242887101018931200: {"language": "de"},
            513792552755789825: {"language": "de"},
        }

        self.strings = {}
        for name in os.listdir("i18n"):
            with open("i18n/" + name) as f:
                self.strings[name.split(".")[0]] = json.load(f)

    def getstr(self, user, strname):
        uconf = self.uconf.get(user.id)
        lang = uconf["language"] if uconf else "en"
        text = self.strings[lang][strname]
        return text

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is None:
            return
        await self.invoke(ctx)
