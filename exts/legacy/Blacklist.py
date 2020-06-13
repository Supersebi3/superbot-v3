import discord
from discord.ext import commands


class Blacklist:
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def blacklist(self, ctx, *, user: discord.User):
        await self.bot.id_blacklist(user.id)
        await ctx.message.add_reaction("\u2611")

    @commands.is_owner()
    @commands.command()
    async def deblacklist(self, ctx, *, user: discord.User):
        await self.bot.id_deblacklist(user.id)
        await ctx.message.add_reaction("\u2611")


def setup(bot):
    bot.add_cog(Blacklist(bot))
