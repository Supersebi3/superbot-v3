import random
from io import BytesIO
from datetime import datetime

import discord
from discord.ext import commands
from PIL import Image
from pilutils.parse import parse


class Misc(commands.Cog):
    @commands.command()
    async def howgay(self, ctx, *, user: discord.User=None):
        you = user is None
        if user is None:
            user = ctx.author  
        now = datetime.utcnow()
        random.seed(user.id*now.month*now.year)
        gayness = random.random()
        if you:
            await ctx.send(f"You are {gayness:.1%} gay.")
        else:
            await ctx.send(f"{user.name} is {gayness:.1%} gay.")


    @commands.command()
    async def color(ctx, *, color):
        try:
            c = parse(color)
        except ValueError:
            return await ctx.send("Color could not be parsed. :(")
        img = Image.new("RGB", (64,64), c)
        img.save(bio := BytesIO(), "png")
        bio.seek(0)
        await ctx.send(str(c), file=discord.File(bio, "color.png"))


def setup(bot):
    bot.add_cog(Misc(bot))
