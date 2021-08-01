import random
import colorsys
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import pilutils
from pilutils.parse import parse, nearest_named_color
from utils import pilcolorblind, checks

import discord
import aiohttp
from discord.ext import commands


def make_palette(colors):
    font = ImageFont.truetype("ProductSans-Bold.ttf", 100)
    background = Image.new("RGB", (1836, 1124))
    positions = [(0, 0), (612, 0), (1224, 0), (0, 562), (612, 562), (1224, 562)]

    for col, pos in zip(colors, positions):
        img = Image.new("RGB", (612, 562), col)
        textcol = (0, 0, 0) if pilutils.luma(col) > 130 else (255, 255, 255)
        d = ImageDraw.Draw(img)
        text = f"#{pilutils.rgb_to_hex(col):06X}"
        textpos = pilutils.align_bbox(
            (0, 0, *img.size), font.getsize(text), align=3, margin=30
        )
        d.text(textpos, text, textcol, font)
        background.paste(img, pos)

    return background


class Graphics(commands.Cog):
    @checks.no_bots()
    @commands.command(aliases=["colour"])
    async def color(self, ctx, *, color=None):
        if not color:
            col = pilutils.random_color()
        else:
            try:
                col = parse(color)
            except ValueError:
                return await ctx.send("Color could not be parsed. :(")

        img = Image.new("RGB", (1080, 720), col)
        font = ImageFont.truetype("ProductSans-Regular.ttf", 50)
        d = ImageDraw.Draw(img)

        h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in col))
        info = {
            "24-bit RGB": ", ".join(map(str, col)),
            "RGB fractions": ", ".join(f"{n/255:.2f}" for n in col),
            "Hex": f"#{pilutils.rgb_to_hex(col):06X}",
            "HSV": ", ".join((f"{h*360:.1f}°", f"{s:.1%}", f"{v:.1%}")),
            "Nearest named color": nearest_named_color(col)[0],
        }

        keystr = "\n".join(info.keys())
        valstr = "\n".join(info.values())

        sp = 24
        textcol = (0, 0, 0) if pilutils.luma(col) > 127 else (255, 255, 255)

        keypos = pilutils.align_bbox(
            (0, 0, *img.size),
            font.getsize_multiline(keystr, spacing=sp),
            align=7,
            margin=25,
            topleft_only=True,
        )
        valpos = pilutils.align_bbox(
            (0, 0, *img.size),
            font.getsize_multiline(valstr, spacing=sp),
            align=9,
            margin=25,
            topleft_only=True,
        )

        d.text(keypos, keystr, textcol, font, spacing=sp)
        d.text(valpos, valstr, textcol, font, align="right", spacing=sp)

        img.save(bio := BytesIO(), "png")
        bio.seek(0)
        await ctx.send(file=discord.File(bio, f"{info['Hex']}.png"))

    @checks.no_bots()
    @commands.command(aliases=["oldcolour"])
    async def oldcolor(self, ctx, *, color=None):
        if not color:
            c = pilutils.random_color()
        else:
            try:
                c = parse(color)
            except ValueError:
                return await ctx.send("Color could not be parsed. :(")
        img = Image.new("RGB", (64, 64), c)
        img.save(bio := BytesIO(), "png")
        bio.seek(0)
        await ctx.send(str(c), file=discord.File(bio, "color.png"))

    @checks.no_bots()
    @commands.command()
    async def palette(self, ctx, *, color=None):
        if not color:
            colors = (
                pilutils.mix(pilutils.random_color(), (255, 255, 255)) for _ in range(6)
            )
        else:
            try:
                base = parse(color)
            except ValueError:
                return await ctx.send("Invalid color.")
            angle = random.choice((120, 180, 240))
            h, s, v = pilutils.rgb_to_hsv(base)
            oh = (h + (angle / 360 * 255)) % 256
            cols = [
                (h, s, 128),
                (h, s, 192),
                (h, s, 255),
                (oh, s, 128),
                (oh, s, 192),
                (oh, s, 255),
            ]
            colors = map(pilutils.hsv_to_rgb, cols)
        img = make_palette(colors)
        img.save(bio := BytesIO(), "png")
        bio.seek(0)
        await ctx.send(file=discord.File(bio, "palette.png"))

    @checks.no_bots()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command()
    async def tpdne(self, ctx, type="person"):
        """Available types: person, cat, horse, artwork"""
        urls = {
            "person": "https://thispersondoesnotexist.com/image",
            "cat": "https://thiscatdoesnotexist.com",
            "horse": "https://thishorsedoesnotexist.com",
            "artwork": "https://thisartworkdoesnotexist.com",
        }
        if type not in urls:
            return await ctx.send("Invalid type.")

        async with aiohttp.request("GET", urls[type]) as resp:
            data = await resp.read()

        bio = BytesIO(data)
        bio.seek(0)
        await ctx.send(file=discord.File(bio, type + ".jpg"))

    @checks.no_bots()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=["colourblind"])
    async def colorblind(self, ctx, *, variant="protanopia"):
        """Available variants:
    prot/protan/protanopia
    deuter/deuteran/deuteranopia
    trit/tritan/tritanopia"""

        variants = {
            "prot": pilcolorblind.protanopia,
            "protan": pilcolorblind.protanopia,
            "protanopia": pilcolorblind.protanopia,
            "deuter": pilcolorblind.deuteranopia,
            "deuteran": pilcolorblind.deuteranopia,
            "deuteranopia": pilcolorblind.deuteranopia,
            "trit": pilcolorblind.tritanopia,
            "tritan": pilcolorblind.tritanopia,
            "tritanopia": pilcolorblind.tritanopia,
        }

        if variant not in variants:
            return await ctx.send(
                "Invalid variant. See `s#help colorblind` for details."
            )

        try:
            attachment = ctx.message.attachments[0]
        except IndexError:
            return await ctx.send("Please attach an image.")

        img = Image.open(BytesIO(await attachment.read())).convert("RGBA")

        func = variants[variant]
        new = await ctx.bot.loop.run_in_executor(None, func, img)

        new.save(bio := BytesIO(), "PNG")
        bio.seek(0)
        await ctx.send(file=discord.File(bio, "colorblind.png"))


def setup(bot):
    bot.add_cog(Graphics(bot))
