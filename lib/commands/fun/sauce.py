import aiohttp
import asyncio
import discord
import gc
from bs4 import BeautifulSoup as bs
from settings import *


async def get(src):
    lst = []
    async with session.post("https://saucenao.com/search.php", data={"url": src}) as response:
        if response.status == 200:
            html = await response.text()
            soup = bs(html, "html.parser")
            results = soup.find_all(name="div", class_="result")
            count = 1
            for result in results:
                if len(lst) == 6:
                    break
                try:
                    if "hidden" in result.get("class"):
                        break
                    result = result.find(name="table", attrs={"class": "resulttable"})
                    obj = result.find(name="div", attrs={"class": "resultimage"}).find(name="img")
                    image_url = obj.get("src")
                    obj = result.find(name="div", attrs={"class": "resultcontentcolumn"}).find(name="a")
                    url = obj.get("href")
                    obj = result.find(name="div", attrs={"class": "resultsimilarityinfo"})
                    similarity = obj.get_text()
                    em = discord.Embed(title=f"Displaying result #{count}", color=0x2ECC71)
                    em.add_field(name="Sauce", value=url, inline=False)
                    em.add_field(name="Similarity", value=similarity, inline=False)
                    em.set_thumbnail(url=image_url)
                    lst.append(em)
                    count += 1
                except:
                    continue
            return lst
        else:
            return lst


@bot.command(name="sauce")
@commands.cooldown(1, 3, commands.BucketType.user)
async def _sauce(cmd, src = None):
    if src is None:
        try:
            src = cmd.message.attachments[0].url
        except:
            await cmd.send("Please attach or provide a URL to the image.")
            return
    results = await get(src)
    n = len(results)
    if n > 0:
        message = await cmd.send(embed=results[0])
        for emoji in choices[:n]:
            await message.add_reaction(emoji)


        def check(reaction, user):
            return str(reaction) in choices[:n] and reaction.message.id == message.id and not user.bot
        

        async def active():
            while True:
                done, pending = await asyncio.wait([bot.wait_for("reaction_add", check=check),
                                                    bot.wait_for("reaction_remove", check=check)],
                                                    return_when=asyncio.FIRST_COMPLETED)
                reaction, user = done.pop().result()
                no = choices.index(str(reaction))
                await message.edit(embed=results[no])


        try:
            await asyncio.wait_for(active(), timeout=300.0)
        except asyncio.TimeoutError:
            await message.clear_reactions()
            del message, results
            gc.collect()
            return
    else:
        await cmd.send("Cannot find the image sauce")
