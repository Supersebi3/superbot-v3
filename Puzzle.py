import discord
from discord.ext import commands


def base4(n):
    if n == 0:
        return "0"
    nums = []
    while n:
        n, r = divmod(n, 4)
        nums.append(str(r))
    return ("".join(nums))[::-1]


class Puzzle(commands.Cog):
    @commands.command()
    async def encode(self, ctx, num1: int, num2: int):
        l = len(bin(max(num1, num2))[2:])
        bin1 = f"{num1:0{l}b}"
        bin2 = f"{num2:0{l}b}"
        t = ""
        for b1, b2 in zip(bin1, bin2):
            b1, b2 = int(b1), int(b2)
            new = 0 if not (b1 + b2) else 1 if b1 > b2 else 2 if b2 > b1 else 3
            t = f"{t}{new}"
        await ctx.send(int(t, 4))

    @commands.command()
    async def decode(self, ctx, num: int):
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

    @commands.command()
    async def tobase(self, ctx, num: int, base: int):
        if not 1 < base < 10:
            await ctx.send("Invalid range.")
            return
        if num == 0:
            await ctx.send("0")
            return
        nums = []
        while num:
            num, r = divmod(num, base)
            nums.append(str(r))
        await ctx.send(("".join(nums))[::-1])


def setup(bot):
    bot.add_cog(Puzzle(bot))
