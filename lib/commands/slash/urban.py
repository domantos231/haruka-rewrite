from settings import *


json = {
    "name": "urban",
    "type": 1,
    "description": "Search Urban Dictionary for a term",
    "options": [{
        "name": "word",
        "description": "The word to look up",
        "type": 3,
        "required": True,
    }]
}


@bot.slash(json)
async def urban_(interaction):
    response = interaction.response
    query = interaction.data["options"][0]["value"]
    await response.defer()
    result = await bot.search_urban(query)
    if result:
        em = result.create_embed()
        em.set_author(
            name = f"This is the definition of {query}",
            icon_url = bot.user.avatar.url,
        )
        await interaction.followup.send(embed = em)
    else:
        await interaction.followup.send(content = "No matching result was found.")