import os

import discord
from discord.ext import commands

from bot import Bot

bot = Bot(command_prefix="s#")


@bot.command()
async def test(ctx):
    await ctx.send("Hi!")


bot.run(os.environ["TOKEN"])
