import os

import discord
from discord.ext import commands
import libneko

bot = libneko.Bot(command_prefix="s#")

@bot.listen('on_ready')
@bot.listen('on_connect')
async def get_owner():
    app_info = await bot.application_info()
    bot.app_info = app_info
    bot.owner_id = app_info.owner.id

bot.load_extension('libneko.extras.superuser')
bot.run(os.environ["TOKEN"])
