import discord
from discord.ext import commands


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def prefix(self, ctx):
        raise commands.MissingRequiredArgument(ctx.command)
    
    @commands.has_permissions(manage_guild=True)
    @prefix.command(name="set")
    async def prefix_set(self, ctx, pre):
        if not pre.strip():
            raise commands.BadArgument("Cannot set empty prefix. Please use "
                    f"`{ctx.prefix}prefix reset` to reset your prefix.")
        id = ctx.guild.id
        await self.bot.set_prefix(id, pre)
        await ctx.send(f"The prefix for this server is now `{pre}`.")

    @commands.has_permissions(manage_guild=True)
    @prefix.command(name="reset")
    async def prefix_reset(self, ctx):
        await self.bot.reset_prefix(ctx.guild.id)
        await ctx.send("The custom prefix for this server has been reset.")

    @prefix.command(name="show")
    async def prefix_show(self, ctx):
        pre = self.bot.prefix_map.get(str(ctx.guild.id))
        if not pre:
            raise commands.BadArgument("This server doesn't have a custom "
                    f"prefix. Use `{ctx.prefix}prefix set` to set a custom "
                    "prefix.")
        await ctx.send(f"The custom prefix of this server is `{pre}`.")


def setup(bot):
    bot.add_cog(Moderation(bot))
