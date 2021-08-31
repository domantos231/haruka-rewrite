from settings import *
from load import *


json = {
    "name": "anime",
    "type": 1,
    "description": "Display the first anime search result from MyAnimeList",
    "options": [{
        "name": "query",
        "description": "The searching query",
        "type": 3,
        "required": True,
    }]
}


@bot.slash(json)
async def anime_(interaction):
    id = interaction.id
    token = interaction.token
    response = interaction.response
    await response.defer()
    query = interaction.data["options"][0]["value"]
    if len(query) < 3:
        await interaction.followup.send(content = "Please provide at least 3 characters in the searching query.")
    else:
        results = await bot.search_anime(query)
        try:
            anime = await bot.get_anime(results[0].id)
            embed = anime.create_embed()
            embed.set_author(
                name = "Displaying the first result",
                icon_url = bot.user.avatar.url,
            )
            embed.set_footer(text = "For all results, consider using the text command")
            await interaction.followup.send(embed = embed)
        except (MyAnimeListException, IndexError):
            await interaction.followup.send(content = "No matching results found.")
