import os
import sys
import logging

import discord
from discord.ext import commands
import libneko

from bot import Bot

<<<<<<< HEAD
__version__ = '0.0.1-p25'
=======
__version__ = '0.0.1-p16'
>>>>>>> 83269fce0a82aeee75b322697a7ae9e4afd6d14c

# install pilutils after new setuptools has been built
os.system("pip install git+https://github.com/Supersebi3/pilutils")

logging.basicConfig(level=logging.INFO)

bot = Bot(command_prefix="s#")


@bot.command()
async def test(ctx):
    await ctx.sendstr(
        "commands.test", sys.version, discord.__version__, libneko.__version__, __version__
    )


@bot.listen()
async def on_ready():
    await bot.change_presence(activity=discord.Game("testing testing testing"))


exts = [
    "libneko.extras.superuser",
    #    "libneko.extras.help",
    "exts.Puzzle",
    "exts.Misc",
    "exts.Graphics",
]


for ext in exts:
    bot.load_extension(ext)


bot.run(os.environ["TOKEN"])

# this is a comment
