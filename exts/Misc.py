import random
import re
from math import prod
from typing import Union
from io import BytesIO, StringIO
from datetime import datetime
import inspect
import textwrap
import unicodedata

import discord
import libneko
from discord.ext import commands
from PIL import Image
from pilutils.parse import parse
from async_tio import Tio


class Misc(commands.Cog):
    @commands.command()
    async def howgay(self, ctx, *, user: Union[discord.User, str] = None):
        """Note: this is not meant to be in any way homophobic, it's just a light hearted gag. Of course, all scores are 100% accurate (not)"""
        you = user is None
        if you:
            user = ctx.author
        now = datetime.utcnow()
        if isinstance(user, str):
            seed = prod(ord(c) + i for i, c in enumerate(user)) * now.month * now.year
        else:
            seed = user.id * now.month * now.year
        random.seed(seed)
        gayness = random.random()
        if now.month == 6:  # pride month
            gayness **= 0.25
        if user == "gay":
            gayness = 1
        if you:
            await ctx.send(f"You are {gayness:.1%} gay.")
        else:
            name = user if isinstance(user, str) else user.name
            await ctx.send(f"{name} is {gayness:.1%} gay.")
        random.seed()

    @commands.command()
    async def source(self, ctx, *, cmd):
        try:
            code = textwrap.dedent(inspect.getsource(ctx.bot.get_command(cmd).callback))
        except AttributeError:
            return await ctx.send(f'Command "{cmd}" not found.')

        fcode = code.replace("`", "\xb4")
        fcode = f"```py\n{fcode}\n```"

        if len(fcode) > 2000:
            sio = StringIO()
            sio.write(code)
            sio.seek(0)
            await ctx.send(file=discord.File(sio, f"{cmd}.py"))

        else:
            await ctx.send(fcode)

    @commands.command()
    async def charinfo(self, ctx, *, chars: str):
        lst = ["`" * 3]
        for ch in chars:
            o = ord(ch)
            if o < 0x100:
                hx = f"\\x{o:02X}"
            elif o < 0x10000:
                hx = f"\\u{o:04X}"
            else:
                hx = f"\\U{o:08X}"
            name = unicodedata.name(ch).title()
            cat = unicodedata.category(ch)
            lst.append(f"- [{ch}]: {hx} ({cat}) - {name}")
        lst.append("`" * 3)

        await ctx.send("\n".join(lst))

    @commands.command(aliases=["run"])
    async def tio(self, ctx, *, arg):
        """Run code using tio.run.

        The first argument should be a code block. The language of the code block specifies the language that the code is assumed to be in.

        Anything after the first code block will be considered input.
        """
        lang_aliases = {
            "py": "python3",
            "python": "python3",
            "js": "javascript",
            "bf": "brainfuck",
        }
        red = discord.Color.red()
        green = discord.Color.green()
        pattern = re.compile(
            r"```(?P<language>\w+)\s*?\n(?P<code>.+?)```(?P<input>.*)", re.DOTALL
        )

        if (m := pattern.match(arg)) is None:
            return await ctx.reply(
                embed=libneko.Embed(color=red, description="\u274c Invalid input.")
            )

        if "code" not in m.groupdict():
            return await ctx.reply(
                embed=libneko.Embed(color=red, description="\u274c No code provided.")
            )
        if "language" not in m.groupdict():
            return await ctx.reply(
                embed=libneko.Embed(
                    color=red, description="\u274c No language provided."
                )
            )

        lang = m["language"].lower()
        lang = lang_aliases.get(lang, lang)
        code = m["code"]
        inp = m.groupdict().get("input", "").strip() or None

        async with await Tio() as tio:
            if lang not in tio.languages:
                return await ctx.reply(
                    embed=libneko.Embed(
                        color=red, description=f"\u274c Unknown language {lang!r}"
                    )
                )

            resp = await tio.execute(code, language=lang, inputs=inp)


        if resp.exit_status == "":
            col = red
            desc = "\u274c Execution timed out."
            foot = False
        else:
            out = resp.stdout or "(no output)"
            if len(out) > 1000:
                out = out[:995] + "[...]"

            col = green if resp.exit_status == "0" else red
            desc = f"**Output: **```\n{out}\n```"
            foot = True

        em = libneko.Embed(color=col, title=lang, description=desc)
        if foot:
            em.set_footer(
                text=f"Took about {resp.real_time} seconds."
            )
        await ctx.reply(embed=em)


def setup(bot):
    bot.add_cog(Misc(bot))
