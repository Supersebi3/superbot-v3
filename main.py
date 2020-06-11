import os
import sys

import discord
from discord.ext import commands

from bot import Bot

bot = Bot(command_prefix="s#")


@bot.command()
async def test(ctx):
    await ctx.send(f"Hi! Python version: ```{sys.version}```dpy version: {discord.__version__}")

bot.load_extension("libneko.extras.superuser")

bot.run(os.environ["TOKEN"])
