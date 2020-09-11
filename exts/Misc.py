import random
from math import prod
from typing import Union
from io import BytesIO, StringIO
from datetime import datetime
import inspect
import textwrap

import discord
from discord.ext import commands
from PIL import Image
from pilutils.parse import parse


class Misc(commands.Cog):
    @commands.command()
    async def howgay(self, ctx, *, user: Union[discord.User, str] = None):
        you = user is None
        if you:
            user = ctx.author
        now = datetime.utcnow()
        if isinstance(user, str):
            seed = prod(ord(c)+i for i, c in enumerate(user)) * now.month * now.year
        else:
            seed = user.id * now.month * now.year
        random.seed(seed)
        gayness = random.random()
        if user == "gay":
            gayness = 1
        if you:
            await ctx.send(f"You are {gayness:.1%} gay.")
        else:
            name = user if isinstance(user, str) else user.name
            await ctx.send(f"{name} is {gayness:.1%} gay.")
        random.seed()


    @commands.command()
    async def source(self, ctx, *, cmd):
        try:
            code = textwrap.dedent(inspect.getsource(ctx.bot.get_command(cmd).callback))
        except AttributeError:
            return await ctx.send(f"Command \"{cmd}\" not found.")
        fcode = code.replace('`', '\xb4')
        fcode = f"```py\n{fcode}\n```"
        if len(fcode) > 2000:
            sio = StringIO()
            sio.write(code)
            sio.seek(0)
            await ctx.send(file=discord.File(sio, f"{cmd}.py"))
        else:
            await ctx.send(fcode)


def setup(bot):
    bot.add_cog(Misc(bot))
