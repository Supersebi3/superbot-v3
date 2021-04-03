import random

import discord
from discord.ext import commands

THORN_SERVER = 820940199609630741


class Þorn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def thorn_react(self, msg):
        if msg.guild.id == THORN_SERVER:
            if "th" in msg.content.lower():
                emoji = self.bot.get_emoji(823566251900403722)
                await msg.add_reaction(emoji)

    @commands.command(aliases=["thornify"])
    async def þornify(self, ctx, *, text: commands.clean_content):
        text = (
            text.replace("th", "þ")
            .replace("Th", "Þ")
            .replace("TH", "Þ")
            .replace("tH", random.choice("Þþ"))
            .replace("t.h", "th")
            .replace("T.h", "Th")
            .replace("T.H", "TH")
            .replace("t.H", "tH")
        )
        await ctx.send(text)


def setup(bot):
    bot.add_cog(Þorn(bot))
