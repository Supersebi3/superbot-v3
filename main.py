import os
import sys

import discord
from discord.ext import commands
import libneko

from bot import Bot

bot = Bot(command_prefix="s#", enable_default_help=False)


@bot.command()
async def test(ctx):
    await ctx.send(f"Hi! Python version: ```{sys.version}```dpy version: {discord.__version__}\nlibneko version: {libneko.__version__}")

bot.load_extension("libneko.extras.superuser")
bot.load_extension("libneko.extras.help")
bot.load_extension("exts.Puzzle")

bot.run(os.environ["TOKEN"])
