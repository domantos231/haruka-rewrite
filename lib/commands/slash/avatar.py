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
    users = interaction.data["resolved"]["users"]
    user_id = list(users.keys())[0]

    avatar_hash = users[user_id]["avatar"]
    user_name = users[user_id]["username"]

    embed = discord.Embed(color = 0x2ECC71)
    embed.set_author(
        name = f"This is {user_name}'s avatar",
        icon_url = bot.user.avatar.url,
    )
    embed.set_image(url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=1024")
    await response.send_message(embed = embed)
