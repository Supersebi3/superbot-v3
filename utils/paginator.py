from collections import OrderedDict as OD
import inspect
import asyncio
import discord


class BasePaginator:
    def __init__(self, pages, **kwargs):
        self.pages = pages
        self.page = 0
        self.maxind = len(pages) - 1
        self.stopped = False
        self.reactions = OD(
            [
                ("\u23ee\ufe0f", self.first),
                ("\u25c0\ufe0f", self.left),
                ("\u25b6\ufe0f", self.right),
                ("\u23ed\ufe0f", self.last),
                ("\U0001f522", self.choose),
                ("\u23f9\ufe0f", self.stop),
                ("\U0001f502", self.slideshow),
            ]
        )
        if len(pages) < 3:
            del self.reactions["\u23ee"]
            del self.reactions["\u23ed"]
            del self.reactions["\U0001f522"]
        if len(pages) == 1:
            del self.reactions["\u25c0"]
            del self.reactions["\u25b6"]
            del self.reactions["\U0001f522"]
            del self.reactions["\U0001f502"]
        for k, v in kwargs:
            setattr(self, k, v)

    def left(self):
        if self.page:
            self.page -= 1
            return True
        return False

    def right(self):
        if self.page < self.maxind:
            self.page += 1
            return True
        return False

    def first(self):
        if self.page:
            self.page = 0
            return True
        return False

    def last(self):
        if self.page < self.maxind:
            self.page = self.maxind
            return True
        return False

    async def stop(self):
        self.stopped = True
        await self.msg.clear_reactions()
        return False

    async def choose(self):
        msg1 = await self.ctx.send(
            "Please tell me the page number you want " "to go to."
        )
        try:
            msg = await self.ctx.bot.wait_for(
                "message",
                timeout=10,
                check=lambda m: m.content.isdigit() and m.author == self.ctx.author,
            )
        except asyncio.TimeoutError:
            await msg1.delete()
            await self.ctx.send("Aborted.", delete_after=1)
            return False
        num = int(msg.content)
        await msg.delete()
        await msg1.delete()
        if not 0 < num < self.maxind + 2:
            await self.ctx.send(
                f"Invalid number ({num}/{self.maxind+1}).", delete_after=1
            )
            return False
        if num == self.page + 1:
            return False
        self.page = num - 1
        return True

    async def slideshow(self):
        await self.msg.clear_reactions()
        for i in range(self.maxind + 1):
            self.page = i
            await self.update()
            await asyncio.sleep(1.5)
        self.page = 0
        await self.update()
        await self.add_reactions()

    async def add_reactions(self):
        for i in self.reactions:
            await self.msg.add_reaction(i)

    async def start(self, ctx):
        """Send the message and return it."""
        pass  # override

    async def update(self):
        """Edit the message corresponding to self.page."""
        pass  # override

    async def run(self, ctx):
        msg = await self.start(ctx)
        self.msg = msg
        self.ctx = ctx
        react = self.reactions
        await self.add_reactions()
        while not self.stopped:
            try:
                reaction, member = await ctx.bot.wait_for(
                    "reaction_add",
                    check=(
                        lambda r, m: r.message.id == msg.id
                        and m == ctx.author
                        and r.emoji in react
                    ),
                    timeout=120,
                )
            except asyncio.TimeoutError:
                await self.stop()
                break
            await msg.remove_reaction(reaction.emoji, member)
            emoji = reaction.emoji
            func = react[emoji]
            res = func()
            if inspect.isawaitable(res):
                res = await res
            if res:
                await self.update()


class EmbedPaginator(BasePaginator):
    def __init__(
        self, embeds, *, title="", color=0, footer=True, footerfmt="{page} / {max}"
    ):
        for i, em in enumerate(embeds):
            if title:
                em.title = title
            if color:
                em.color = color
            if footer:
                em.set_footer(text=footerfmt.format(page=i + 1, max=len(embeds)))
        super().__init__(embeds)

    async def start(self, ctx):
        msg = await ctx.send(embed=self.pages[0])
        return msg

    async def update(self):
        await self.msg.edit(embed=self.pages[self.page])

    @classmethod
    def fromplaintext(cls, lst, **kwargs):
        embeds = [discord.Embed(description=i) for i in lst]
        return cls(embeds, **kwargs)


class PlainTextPaginator(BasePaginator):
    def __init__(self, pages, *, fmt="{text}\n\n**Page {page} / {max}**"):
        pg = [
            fmt.format(text=text, page=i + 1, max=len(pages))
            for i, text in enumerate(pages)
        ]
        super().__init__(pg)

    async def start(self, ctx):
        msg = await ctx.send(self.pages[0])
        return msg

    async def update(self):
        await self.msg.edit(content=self.pages[self.page])
