import os
import discord
from discord.ext import commands
import libneko

bot = libneko.Bot(command_prefix="s#")

@bot.listen()
async def on_start():
    await bot.get_user(242887101018931200).send("I'm ready!")

bot.run(os.environ["TOKEN"])