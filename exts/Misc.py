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


def setup(bot):
    bot.add_cog(Misc(bot))
