import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import pilutils
from pilutils.parse import parse

import discord
from discord.ext import commands


def luma(rgb):
    r, g, b = rgb
    l = r * 299 / 1000 + g * 587 / 1000 + b * 114 / 1000
    return l


font = ImageFont.truetype("ProductSans-Bold.ttf", 100)


def make_palette(colors):
    background = Image.new("RGB", (1836, 1124))
    positions = [(0, 0), (612, 0), (1224, 0), (0, 562), (612, 562), (1224, 562)]

    for col, pos in zip(colors, positions):
        img = Image.new("RGB", (612, 562), col)
        textcol = (0, 0, 0) if luma(col) > 130 else (255, 255, 255)
        d = ImageDraw.Draw(img)
        text = f"#{pilutils.rgb_to_hex(col):06X}"
        textpos = pilutils.align_bbox(
            (0, 0, *img.size), font.getsize(text), align=3, margin=30
        )
        d.text(textpos, text, textcol, font)
        background.paste(img, pos)

    return background


class Graphics(commands.Cog):
    @commands.command()
    async def color(self, ctx, *, color):
        try:
            c = parse(color)
        except ValueError:
            return await ctx.send("Color could not be parsed. :(")
        img = Image.new("RGB", (64, 64), c)
        img.save(bio := BytesIO(), "png")
        bio.seek(0)
        await ctx.send(str(c), file=discord.File(bio, "color.png"))

    @commands.command()
    async def palette(self, ctx):
        colors = (
            pilutils.mix(pilutils.random_color(), (255, 255, 255)) for _ in range(6)
        )
        img = make_palette(colors)
        img.save(bio := BytesIO(), "png")
        await ctx.send(file=discord.File(bio, "palette.png"))


def setup(bot):
    bot.add_cog(Graphics(bot))
