import discord
from settings import *


json = {
    "name": "avatar",
    "type": 1,
    "description": "Get the avatar from a user.",
    "options": [{
        "name": "user",
        "description": "The target user to get the avatar from",
        "type": 6,
        "required": True,
    }]
}


@bot.slash(json)
async def avatar_(interaction):
    response = interaction.response
    user_id = int(list(interaction.data["resolved"]["users"].keys())[0])
    user = bot.get_user(user_id)
    if user:
        embed = discord.Embed(color = 0x2ECC71)
        embed.set_author(
            name = f"This is {user.name}'s avatar",
            icon_url = bot.user.avatar.url,
        )
        embed.set_image(url = user.avatar.url)
        await response.send_message(embed = embed)
    else:
        await response.send_message(content = "Cannot find this user.")
