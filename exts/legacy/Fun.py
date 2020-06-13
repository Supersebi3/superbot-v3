import time
import random
import discord
from discord.ext import commands
import asyncio
import checks


class Fun:
    def __init__(self, bot):
        self.bot = bot

    @checks.no_bots()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases="pang peng pong \U0001F3D3".split())
    async def ping(self, ctx):
        """Test the bot's latency."""
        m = await ctx.send("Please wait...")
        t1 = ctx.message.created_at
        t2 = m.created_at
        time = (t2-t1).total_seconds() * 1000
        ver = ctx.invoked_with
        conversions = {
                "ping": "\U0001F3D3 Pong! Took",
                "pong": "\U0001F3D3 Ping! Took",
                "pang": "\U0001F52B Peng! You've been hit after",
                "peng": "\U0001F52B Pang! You've been hit after",
                "\U0001F3D3": "\U0001F3D3 Took"
                }
        fmt = "{} {:.0f}ms! (Heartbeat: {:.0f}ms)"
        text = fmt.format(conversions[ver], time, self.bot.latency*1000)
        await m.edit(content=text)

    @checks.no_bots()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def pings(self, ctx):
        """Test the bot's latency."""
        m = await ctx.send("Please wait...")
        time1 = int((m.created_at-ctx.message.created_at).total_seconds()*1000)
        before = time.monotonic()
        await (await self.bot.ws.ping())
        after = time.monotonic()
        time2 = int((after - before) * 1000)
        time3 = int(self.bot.latency * 1000)
        em = (discord.Embed(color=discord.Colour.green(), title="Pings")
                .add_field(name="Message difference", value=f"{time1}ms")
                .add_field(name="Websocket ping", value=f"{time2}ms")
                .add_field(name="Heartbeat latency", value=f"{time3}ms")
            )
        await m.edit(content=None, embed=em)

    @checks.no_bots()
    @commands.command()
    async def say(self, ctx, channel: commands.clean_content, *,
            text: commands.clean_content = ""):
        """Make me say something."""
        try:
            dest = await commands.TextChannelConverter().convert(
                    ctx, channel)
        except commands.BadArgument:
            dest = ctx
            text = f"{channel} {text}"
        await dest.send(text)
        await ctx.message.delete()

    @checks.no_bots()
    @commands.command()
    async def reverse(self, ctx, *, text:commands.clean_content):
        """Make me reverse some text."""
        await ctx.send(text[::-1].replace("@", "@\u200b"))

    @commands.command()
    async def dice(self, ctx):
        """Roll a dice."""
        await ctx.send(random.randint(1, 6))

    @commands.command()
    async def coin(self, ctx):
        """Throw a coin."""
        await ctx.send(random.choice(["Heads", "Tails"]))

    @commands.command()
    async def rps(self, ctx, choice):
        choice = choice.lower()
        conv = {"r": 1, "p": 2, "s": 3, "rock": 1, "paper": 2, "scissors": 3}
        rconv = None, "rock", "paper", "scissors"
        if choice not in conv:
            raise commands.BadArgument(f"Invalid choice '{choice}'.")
        pnum = conv[choice]
        cnum = random.randint(1, 3)
        diff = pnum - cnum
        if diff in (1, -2):
            res = "You won!"
        elif diff in (2, -1):
            res = "You lost..."
        else:
            res = "It's a draw."
        text = f"""You: {rconv[pnum]}
Computer: {rconv[cnum]}
{res}"""
        await ctx.send(text)

    @commands.command(usage="[elem 1]|[elem 2]|[elem 3]|...\\[suffix]")
    async def choose(self, ctx, *, things: commands.clean_content):
        ssplit = things.split("\\")
        suffix = ssplit[-1] if len(ssplit) > 1 else ""
        options = ssplit[0].split("|")
        await ctx.send(f"{random.choice(options).strip()} {suffix.strip()}")

    @commands.command()
    async def hi(self, ctx):
        await ctx.send(f"Hello, {ctx.author.mention}!")

    @checks.no_bots()
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command()
    async def repeat(self, ctx, num: int, *, text: commands.clean_content):
        if "spam" not in ctx.channel.name:
            raise commands.BadArgument("This command is only "
                    "available in spam channels.")
        ssplit = text.split("\\")
        suffix = ssplit[-1] if len(ssplit) > 1 else ""
        text = ssplit[0]
        num = min(num, 50)
        fmt = (text.replace("%count%", "{0}")
                    .replace("%countBackwards%", "{1}")
                    .replace("%enumerate%", "{2}")
               )
        for i in range(1, num+1):
            if i % 10 == 1 and i != 11:
                enumend = "st"
            elif i % 10 == 2 and i != 12:
                enumend = "nd"
            elif i % 10 == 3 and i != 13:
                enumend = "rd"
            else:
                enumend = "th"
            text = fmt.format(i, num - i + 1, f"{i}{enumend}")
            await ctx.send(text)
            await asyncio.sleep(2)
        if suffix:
            await ctx.send(suffix)

    @commands.command()
    async def typing(self, ctx, time: float = 10):
        await ctx.message.delete()
        async with ctx.channel.typing():
            await asyncio.sleep(time)

    @commands.command()
    async def embed(self, ctx, color: discord.Color, *, text):
        em = discord.Embed(description=text, color=color)
        await ctx.send(embed=em)
        await ctx.message.delete()

    @commands.command()
    async def emojify(self, ctx, *, text):
        o = ""
        conv = (":zero: :one: :two: :three: :four: :five: :six: :seven: "
                ":eight: :nine:").split()
        for c in text.lower():
            if c in "abcdefghijklmnopqrstuvwxyz":
                o += f":regional_indicator_{c}:"
            elif c == " ":
                o += c
            elif c in "0123456789":
                o += conv[int(c)]
            else:
                o += {"*": ":asterisk:", "#": ":hash:"}.get(c, "")
        if o:
            await ctx.send(o)

    @commands.command()
    async def emoji(self, ctx, name):
        em = discord.utils.find(lambda e: e.name.lower() == name.lower(), 
                self.bot.emojis)
        if em is None:
            raise commands.BadArgument(f"No emoji called {name} found.")
        await ctx.send(em)
        await ctx.message.delete()

    @commands.command()
    async def memory(self, ctx, time: float = 3.0, digits: int = 7):
        if time > 10:
            raise commands.BadArgument(f"Sorry, but a time of {time} seconds "
                    "is too easy :P")
        if not 0 < digits < 100:
            raise commands.BadArgument("Invalid number of digits.")
        nmin = 10 ** (digits - 1)
        nmax = (10 ** digits) - 1
        num = random.randint(nmin, nmax)
        await ctx.send(f"{ctx.author.mention}, remember this number:\n{num}",
                delete_after=time)
        msg = await self.bot.wait_for("message", 
                check=(lambda m: m.author == ctx.author 
                    and m.channel == ctx.channel and m.content.isdigit()))
        if msg.content == str(num):
            await ctx.send(f"GG! {num} is correct!")
        else:
            await ctx.send(f"Nope. It was {num}")

    @checks.no_bots()
    @commands.command()
    async def randomchars(self, ctx, num: int = 100, max: int = 0x10FFFF):
        if not 0 < num < 2001:
            raise commands.BadArgument("Invalid number of characters.")
        if not 32 < max < 0x110000:
            raise commands.BadArgument("Invalid unicode range.")
        await ctx.send("".join([chr(random.randint(0, max))
            for i in range(num)]))

    @commands.command()
    async def vaporwave(self, ctx, *, text):
        o = ""
        for c in text:
            if c == " ":
                c = "\u3000"
            elif ord(c) in range(33, 127):
                c = chr(ord(c) + 0xFEE0)
            o += c
        await ctx.send(o)

    @commands.command()
    async def testi18n(self, ctx):
        await ctx.sendstr('sample')


def setup(bot):
    bot.add_cog(Fun(bot))
