import os
import discord
from discord.ext import commands
import libneko

bot = libneko.Bot(command_prefix="s#")

bot.run(os.environ["TOKEN"])