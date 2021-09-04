import discord
from settings import *


json = {
    "name": "info",
    "type": 1,
    "description": "Get the information about a user.",
    "options": [{
        "name": "user",
        "description": "The target user to retrieve information about.",
        "type": 6,
        "required": True,
    }]
}


@bot.slash(json)
async def info_(interaction):
    response = interaction.response
    if not isinstance(interaction.channel, discord.TextChannel):
        return await response.send_message("This command can only be used in a server text channel.")
    user_id = int(list(interaction.data["resolved"]["users"].keys())[0])
    user = interaction.guild.get_member(user_id)
    if user:
        await response.send_message(embed = bot.user_info(user))
    else:
        await response.send_message("Cannot find this user.")