from settings import *


json = {
    "name": "say",
    "type": 1,
    "description": "Say something - a very useful command",
    "options": [{
        "name": "content",
        "description": "The string to repeat",
        "type": 3,
        "required": True,
    }]
}


@bot.slash(json)
async def say_(interaction):
    response = interaction.response
    await response.send_message(content = interaction.data["options"][0]["value"])
