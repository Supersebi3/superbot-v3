import libneko

from context import Context


class Bot(libneko.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uconf = {}

        self.strings = {}
        for name in os.listdir('i18n'):
            with open('i18n/'+name) as f:
                self.strings[name[:2]] = json.load(f)


    async def process_commands(self, message):
    ctx = await self.get_context(message, cls=Context)
    if ctx.command is None:
        return
    await self.invoke(ctx)