import discord
from discord.ext import commands
import logging


class Events:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            helpcmd = self.bot.get_command("help")
            await ctx.invoke(helpcmd, *ctx.command.qualified_name.split())
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"\u2744 {error!s}", delete_after=3)
        elif isinstance(error, (commands.BadArgument,
            commands.MissingPermissions)):
            await ctx.send(f"\u274C {error!s}", delete_after=3)
        elif isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("\u2753")
        elif isinstance(error, commands.NotOwner):
            await ctx.send(f"\U0001F621 {error!s}", delete_after=3)
        else:
            logging.error(f"{type(error).__name__} (Command {ctx.command!s}):"
                    f"{error!s}")

    async def on_guild_join(self, guild):
        if guild.system_channel:
            text = ("Thanks for adding me to your server!\n\nUse "
            "`{prefix}help` to get a list of all commands.\nIf you have any "
            "suggestions for this bot, send them with `{prefix}suggest`!")
            formatted = text.format(prefix=self.bot.config.prefix)
            await guild.system_channel.send(formatted)
        text2 = f"I just got added to the server `{guild.name}`."
        await self.bot.get_user(self.bot.owner_id).send(text2)
        await self.bot.update_game()

    async def on_guild_remove(self, guild):
        text = f"I just got removed from the server `{guild.name}`."
        await self.bot.get_user(bot.owner_id).send(text)
        await self.bot.update_game()

    async def on_guild_channel_create(self, channel):
        if not isinstance(channel, discord.TextChannel):
            return
        try:
            await channel.send("First")
        except discord.Forbidden:
            pass


def setup(bot):
    bot.add_cog(Events(bot))
