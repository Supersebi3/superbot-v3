from discord.ext import commands


def no_bots():
    def inner(ctx):
        return not ctx.author.bot

    return commands.check(inner)
