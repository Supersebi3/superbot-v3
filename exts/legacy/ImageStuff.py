import os
import functools
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import checks


class ImageStuff:
    def __init__(self, bot):
        self.bot = bot

    @checks.no_bots()
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.command()
    async def captcha(self, ctx, type, *, text):
        type = type.lower()
        if type not in "checked unchecked loading".split():
            raise commands.BadArgument(f"Invalid type {type!r}. Available "
                    "types: `unchecked`, `loading`, `checked`")
        font = ImageFont.truetype("Roboto-Regular.ttf", 14)
        async with ctx.typing():
            img = Image.open(f"blank-captcha-{type}.png")
            img.load()
            d = ImageDraw.Draw(img)
            fnc = functools.partial(d.text, (53,30), text, fill=(0,0,0,255),
                    font=font)
            await self.bot.loop.run_in_executor(None, fnc)
            img.save("captcha.png")
        await ctx.send(file=discord.File("captcha.png"))
        os.system("rm captcha.png")
        img.close()


def setup(bot):
    bot.add_cog(ImageStuff(bot))
