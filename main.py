import os

import discord
from discord.ext import commands
import libneko

print(libneko.__version__)

from bot import Bot

bot = Bot(command_prefix="s#")

@bot.command()
async def test(ctx):
    await ctx.send("Hi!")

bot.load_extension("libneko.extras.superuser")
bot.run(os.environ["TOKEN"])
