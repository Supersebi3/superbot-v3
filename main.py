import os

import discord
from discord.ext import commands
import libneko

from bot import Bot

bot = Bot(command_prefix="s#")

@bot.listen()
async def on_connect():
    app_info = await bot.application_info()
    bot.app_info = app_info
    bot.owner_id = app_info.owner_id

bot.load_extension("libneko.extras.superuser")
bot.run(os.environ["TOKEN"])