import aiohttp
import asyncio
import discord
from settings import *


@bot.command(
    name = "sauce",
    description = "Find the image source with saucenao",
    usage = "sauce <URL to image or attachment>",
)
@commands.cooldown(1, 6, commands.BucketType.user)
async def _sauce(cmd, src = None):
    if src is None:
        try:
            src = cmd.message.attachments[0].url
        except:
            await cmd.send("Please attach or provide a URL to the image.")
            return
    results = await bot.get_sauce(src)
    n = len(results)
    if n > 0:
        msg = await cmd.send(embed=results[0])
        for emoji in choices[:n]:
            await msg.add_reaction(emoji)


        def check(reaction, user):
            return reaction.message.id == msg.id and str(reaction) in choices[:n] and not user.bot
        

        async def active():
            while True:
                done, pending = await asyncio.wait([bot.wait_for("reaction_add", check=check),
                                                    bot.wait_for("reaction_remove", check=check)],
                                                    return_when = asyncio.FIRST_COMPLETED)
                reaction, user = done.pop().result()
                no = choices.index(str(reaction))
                await msg.edit(embed=results[no])


        try:
            await asyncio.wait_for(active(), timeout=300.0)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            return
    else:
        await cmd.send("Cannot find the image sauce")
