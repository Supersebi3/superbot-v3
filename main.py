import os
import sys
import logging
from io import BytesIO

import discord
from discord.ext import commands
import libneko
from PIL import Image
from pilutils.parse import parse

from bot import Bot

logging.basicConfig(level=logging.INFO)

bot = Bot(command_prefix="s#", enable_default_help=False)


@bot.command()
async def test(ctx):
    await ctx.send(f"Hi! Python version: ```{sys.version}```dpy version: {discord.__version__}\nlibneko version: {libneko.__version__}")

@bot.command()
async def color(ctx, *, color):
    try:
        c = parse(color)
    except ValueError:
        return await ctx.send("Color could not be parsed. :(")
    img = Image.new("RGB", (64,64), c)
    img.save(bio := BytesIO(), "png")
    bio.seek(0)
    await ctx.send(file=discord.File(bio, "color.png"))

@bot.listen()
async def on_ready():
    await bot.change_presence(activity=discord.Game("testing testing testing"))

bot.load_extension("libneko.extras.superuser")
bot.load_extension("libneko.extras.help")
bot.load_extension("exts.Puzzle")

bot.run(os.environ["TOKEN"])
