import discord
from discord.ext import commands
from utils import checks


def base4(n):
    if n == 0:
        return "0"
    nums = []
    while n:
        n, r = divmod(n, 4)
        nums.append(str(r))
    return ("".join(nums))[::-1]


class Puzzle(commands.Cog):
    @checks.no_bots()
    @commands.command()
    async def encode(self, ctx, num1: int, num2: int):
        """Encode a pair of numbers. Encode how? That's for you to find out!"""
        l = len(bin(max(num1, num2))[2:])
        bin1 = f"{num1:0{l}b}"
        bin2 = f"{num2:0{l}b}"
        t = ""
        for b1, b2 in zip(bin1, bin2):
            b1, b2 = int(b1), int(b2)
            new = 0 if not (b1 + b2) else 1 if b1 > b2 else 2 if b2 > b1 else 3
            t = f"{t}{new}"
        await ctx.send(int(t, 4))

    @checks.no_bots()
    @commands.command()
    async def decode(self, ctx, num: int):
        """Reverse the encoding."""
        b4 = base4(num)
        num1 = 0
        num2 = 0
        f = 1
        for q in b4[::-1]:
            if int(q) in (1, 3):
                num1 += f
            if int(q) in (2, 3):
                num2 += f
            f *= 2
        await ctx.send((num1, num2))

    @checks.no_bots()
    @commands.command()
    async def tobase(self, ctx, num: int, base: int):
        """Convert any integer to any base between 2 and 36."""
        if not 1 < base < 37:
            await ctx.send("Invalid base.")
            return
        conv = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if num == 0:
            await ctx.send("0")
            return
        digs = []
        while num:
            num, r = divmod(num, base)
            digs.append(conv[r])
        await ctx.send(("".join(digs))[::-1])


def setup(bot):
    bot.add_cog(Puzzle(bot))
