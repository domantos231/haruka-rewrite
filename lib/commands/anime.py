import mal
import discord
from lib.settings import *


@bot.command()
async def anime(cmd, *, arg = None):
    if arg == None:
        await cmd.send("Please specify an anime name!")
    else:
        search = mal.AnimeSearch(arg, timeout=1)
        desc = ""
        for i in range(6):
            anim = search.results[i]
            desc += f"**#{i+1}** {anim.title}\n"
        anime_em = discord.Embed(title=f"Top 6 search results for {arg}", description=desc, color=0x2ECC71)
        anime_em.set_footer(text="From myanimelist.net")
        message = await cmd.send(embed=anime_em)
        for emoji in choices:
            await message.add_reaction(emoji)
        reaction = ""
        def check(reaction, user):
            return reaction.message.id == message.id and not user.bot
        while not str(reaction) in choices:
            reaction, user = await bot.wait_for("reaction_add", check=check)
        choice = choices.index(str(reaction))
        obj = mal.Anime(search.results[choice].mal_id)
        anime_em = discord.Embed(
            title=obj.title, description=obj.synopsis, color=0x2ECC71
        )
        genre_str = ""
        for genre in obj.genres:
            genre_str += genre + ", "
        anime_em.set_thumbnail(url=obj.image_url)
        anime_em.add_field(
            name="Japanese Title", value=obj.title_japanese, inline=False
        )
        anime_em.add_field(name="Genres", value=genre_str[:-2], inline=False)
        anime_em.add_field(name="Aired", value=obj.aired, inline=True)
        anime_em.add_field(name="Ranking", value=obj.rank, inline=True)
        anime_em.add_field(name="Rating", value=obj.rating, inline=True)
        anime_em.add_field(name="Score", value=obj.score, inline=True)
        anime_em.add_field(name="Episodes", value=obj.episodes, inline=True)
        anime_em.add_field(name="Status", value=obj.status, inline=True)
        anime_em.add_field(
            name="Reference", value=f"[MyAnimeList link]({obj.url})", inline=False
        )
        anime_em.set_footer(text="From myanimelist.net")
        await cmd.send(embed=anime_em)
