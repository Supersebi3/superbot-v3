from discord.ext import commands
import time
import datetime
import math
import asyncio
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import os
import sys
import random
import inspect
import io
import json
import re
import unicodedata

class REPL:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        'Automatically removes code blocks from the code.'
        if (content.startswith('```') and content.endswith('```')):
            return '\n'.join(content.split('\n')[1:(- 1)])
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if (e.text is None):
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @commands.is_owner()
    @commands.command(name='exec')
    async def _exec(self, ctx, *, body: str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
            'ns': self.bot.namespace,
        }
        env.update(globals())
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')
        paginator = commands.Paginator(prefix="```py\n", suffix="\n```", max_size=2000)
        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(self.get_syntax_error(e))
        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            for line in "{}{}".format(value, traceback.format_exc()).splitlines():
                paginator.add_line(line)
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2611')
            except:
                pass
            if (ret is None):
                if value:
                    for line in value.splitlines():
                        paginator.add_line(line)
            else:
                self._last_result = ret
                for line in ("%s%s" % (value, ret)).splitlines():
                    paginator.add_line(line)
        for page in paginator.pages:
            await ctx.send(page)

    @commands.is_owner()
    @commands.command()
    async def repl(self, ctx):
        msg = ctx.message
        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': msg,
            'guild': msg.guild,
            'channel': msg.channel,
            'author': msg.author,
            '_': None,
            'ns': self.bot.namespace,
            'self': self,
        }
        variables.update(globals())
        if (msg.channel.id in self.sessions):
            await ctx.send('Already running a REPL session in this channel. Exit it with `quit`.')
            return
        self.sessions.add(msg.channel.id)
        await ctx.send('Enter code to execute or evaluate. `exit()` or `quit` to exit.')
        while True:
            response = await self.bot.wait_for('message', check=(lambda m: m.content.startswith('`') and m.author.id == self.bot.owner_id and m.channel == ctx.channel))
            cleaned = self.cleanup_code(response.content)
            if (cleaned in ('quit', 'exit', 'exit()')):
                await ctx.send('Exiting.')
                self.sessions.remove(msg.channel.id)
                return
            paginator = commands.Paginator(prefix="```py\n", suffix="\n```", max_size=2000)
            executor = exec
            if (cleaned.count('\n') == 0):
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval
            if (executor is exec):
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await ctx.send(self.get_syntax_error(e))
                    continue
            variables['message'] = response
            fmt = None
            stdout = io.StringIO()
            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = '{}{}'.format(value, traceback.format_exc())
            else:
                value = stdout.getvalue()
                if (result is not None):
                    fmt = '{}{!r}'.format(value, result)
                    variables['_'] = result
                elif value:
                    fmt = '{}'.format(value)
            try:
                if (fmt is not None):
                    for line in fmt.splitlines():
                        try:
                            paginator.add_line(line)
                        except RuntimeError:
                            splitted = [line[i:i+1988] for i in range(0, len(line), 1988)]
                            for part in splitted:
                                paginator.add_line(part)
                    for page in paginator.pages:
                        await msg.channel.send(page)
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await msg.channel.send('Unexpected error: `{}`'.format(e))

    @commands.is_owner()
    @commands.command()
    async def system(self, ctx, *, command):
        if (not await self.bot.loop.run_in_executor(None, os.system, command)):
            await ctx.message.add_reaction('\u2611')
        else:
            await ctx.message.add_reaction('\u274C')

    @commands.is_owner()
    @commands.command()
    async def source(self, ctx, *, command):
        cmd = inspect.getsource(self.bot.get_command(command).callback)
        await ctx.send(f"```py\n{cmd}\n```")

    @commands.is_owner()
    @commands.command()
    async def sql(self, ctx, *, command):
        try:
            await self.bot.psqlcur.execute(command)
            await ctx.message.add_reaction('\u2611')
        except Exception as e:
            await ctx.send(f"```py\n{e!s}\n```")
        if command.lower().startswith("select"):
            res = await self.bot.psqlcur.fetchall()
            await ctx.send(f"```py\n{res}\n```")
        self.bot.psqlcon.commit()

def setup(bot):
    bot.add_cog(REPL(bot))
