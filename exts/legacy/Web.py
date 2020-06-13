import textwrap
from urllib.parse import quote as uriquote
import discord
from discord.ext import commands
import checks

class Web:
    def __init__(self, bot):
        self.bot = bot

    @checks.no_bots()
    @commands.command()
    async def headlines(self, ctx, *, query=""):
        urlfmt = "http://newsapi.org/v2/top-headlines?language=en&q={}"
        headers = {
            "x-api-key": self.bot.config.apikeys["newsapi"]
        }
        url = urlfmt.format(uriquote(query))
        async with self.bot.aio_session.get(url, headers=headers) as r:
            resp = await r.json()
        if resp["status"] != "ok":
            err = resp["message"]
            await ctx.send("The following error occured while running the "
                    f"command: ```{err}```Please report this to the bot "
                    "owner.")
            return
        articles = resp["articles"][:3]
        em = discord.Embed(title="News by NewsAPI.org",
                url="http://newsapi.org", color=discord.Color.green())
        for art in articles:
            fname = f"[{art['title']}]({art['url']})"
            fname = art['title'] if len(fname) > 256 else fname
            fval = textwrap.shorten(art["description"] or "[...]", 140)
            em.add_field(name=fname, value=fval or "[...]")
        await ctx.send(embed=em)

    @checks.no_bots()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def norris(self, ctx, fname="Chuck", lname="Norris"):
        urlfmt = ("http://api.icndb.com/jokes/random?firstName={}&lastName={}"
                "&escape=javascript")
        url = urlfmt.format(uriquote(fname), uriquote(lname))
        async with self.bot.aio_session.get(url) as r:
            data = await r.json()
        joke = data["value"]["joke"].replace("\\", "")
        await ctx.send(joke)

    @checks.no_bots()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def nerdnorris(self, ctx, fname="Bill", lname="Gates"):
        urlfmt = ("http://api.icndb.com/jokes/random?firstName={}&lastName={}"
                "&escape=javascript&limitTo=[nerdy]")
        url = urlfmt.format(uriquote(fname), uriquote(lname))
        async with self.bot.aio_session.get(url) as r:
            data = await r.json()
        joke = data["value"]["joke"].replace("\\", "")
        await ctx.send(joke)

    @checks.no_bots()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def latex(self, ctx, fmt, *, latex):
        host = "http://63.142.251.124:80"
        d = {"code": latex, "format": fmt}
        async with self.bot.aio_session.post(f"{host}/api/v2", data=d) as r:
            res = await r.json()
        if res["status"] != "success":
            error = res["description"]
            await ctx.send(f"Something went wrong: ```{error}```"
                           "Please report this to Supersebi3#3525.")
            return
        file = res["filename"]
        async with self.bot.aio_session.get(f"{host}/api/v2/{file}") as r2:
            res2 = await r2.read()
        await ctx.send(file=discord.File(res2, f"latex.{fmt}"))

    @commands.is_owner()
    @commands.command()
    async def greek(self, ctx, *, word):
        desc = (f"[Wiktionary](https://en.wiktionary.org/wiki/{word}#Greek)\n"
                f"[WordReference](https://wordreference.com/gren/{word})\n"
                f"[cooljugator{' (Not a verb tho)' if not (word.endswith('ω') or word.endswith('ώ') or word.endswith('ομαι') or word.endswith('όμαι')) else ''}](https://cooljugator.com/gr/{word})\n"
        )
        em = discord.Embed(title=word, description=desc)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Web(bot))
