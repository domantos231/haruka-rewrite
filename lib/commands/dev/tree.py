import asyncio
import discord
from settings import *


@bot.command(name="tree")
async def _tree(cmd):
    if await bot.is_owner(cmd.author):
        process = await asyncio.create_subprocess_shell(rf"find {root} | sed -e 's/[^-][^\/]*\//  |/g' -e 's/|\([^ ]\)/|-\1/' > {root}/tree.txt")
        await process.wait()
        await cmd.send(content="This is the tree of the root directory", file=discord.File(f"{root}/tree.txt"))
    else:
        await cmd.send("This command is for developers only.")
    