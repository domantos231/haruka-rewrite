import discord
from settings import *


json = {
    "name": "svinfo",
    "type": 1,
    "description": "Get the information about the server.",
}


@bot.slash(json)
async def svinfo_(interaction):
    response = interaction.response
    if not interaction.guild:
        await response.send_message("This command can only be used in a server.")
    else:
        em = bot.server_info(interaction.guild)
        await response.send_message(embed = em)