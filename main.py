import os
import sys
import logging

import discord
from discord.ext import commands
import libneko

from bot import Bot

# install pilutils after new setuptools has been built
os.system("pip install git+https://github.com/Supersebi3/pilutils")

logging.basicConfig(level=logging.INFO)

bot = Bot(command_prefix="s#", enable_default_help=False)


@bot.command()
async def test(ctx):
    await ctx.sendstr("commands.test", sys.version, discord.__version__, libneko.__version__)

@bot.listen()
async def on_ready():
    await bot.change_presence(activity=discord.Game("testing testing testing"))

bot.load_extension("libneko.extras.superuser")
#bot.load_extension("libneko.extras.help")
bot.load_extension("exts.Puzzle")
bot.load_extension("exts.Misc")

bot.run(os.environ["TOKEN"])
