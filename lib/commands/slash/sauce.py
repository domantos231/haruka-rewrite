from settings import *


json = {
    "name": "sauce",
    "type": 1,
    "description": "Find the image source with saucenao",
    "options": [{
        "name": "url",
        "description": "The URL to the image",
        "type": 3,
        "required": True,
    }]
}


@bot.slash(json)
async def sauce_(interaction):
    id = interaction.id
    token = interaction.token
    response = interaction.response
    await response.defer()
    results = await bot.get_sauce(interaction.data["options"][0]["value"])
    if not results:
        await interaction.followup.send(content = "Cannot find the image sauce.")
    else:
        embed = results[0]
        embed.title = "Displaying the first result"
        embed.set_footer(text = "For all results, consider using the text command")
        await interaction.followup.send(embed = embed)
