import os
import sys
import logging

import discord
import libneko
from discord.ext import commands

from bot import Bot

__version__ = '0.0.1-p80'

# install pilutils after new setuptools has been built
os.system("pip install git+https://github.com/Supersebi3/pilutils")

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
#intents.message_content = True

bot = Bot(command_prefix="s#", intents=intents)


@bot.command()
async def test(ctx):
    await ctx.sendstr(
        "commands.test",
        sys.version,
        discord.__version__,
        libneko.__version__,
        __version__,
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
    "exts.Thorn",
]


for ext in exts:
    bot.load_extension(ext)


bot.run(os.environ["TOKEN"])
