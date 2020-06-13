from collections import OrderedDict as OD
import discord
from discord.ext import commands
from paginator import EmbedPaginator
import checks

class Help:

    @checks.no_bots()
    @commands.command(hidden=True)
    async def embedhelp(self, ctx, *args):
        bot = ctx.bot
        # dest = ctx.author if bot.pm_help else ctx

        async def can_run(ctx, cmd):
            try:
                await cmd.can_run(ctx)
                return True
            except commands.CommandError:
                return False

        if not args:
            # normal help
            cogs = OD()
            nocat = []
            for cmd in sorted(bot.commands, key=lambda c: c.name.lower()):
                if cmd.hidden or not (await can_run(ctx, cmd)):
                    continue
                cname = cmd.cog_name
                if not cname:
                    nocat.append(cmd)
                elif cname in cogs:
                    cogs[cname].append(cmd)
                else:
                    cogs[cname] = [cmd]

            if nocat:
                cogs["No Category"] = nocat

            pages = []
            for k, v in cogs.items():
                em = discord.Embed()
                em.set_author(name=k)
                for c in v:
                    name = c.name
                    val = "\u200b"
                    if c.short_doc:
                        val = c.short_doc
                    em.add_field(name=name, value=val)
                pages.append(em)
            pg = EmbedPaginator(pages, color=discord.Color.green(),
                    title="Help")
            await pg.run(ctx)
        elif len(args) == 1:
            pass # TODO

def setup(bot):
    bot.add_cog(Help())
