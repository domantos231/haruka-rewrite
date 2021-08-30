import discord
from settings import *


@bot.event
async def on_interaction(interaction):
    """Execute slash commands"""
    if isinstance(interaction.channel, discord.TextChannel):
        data = interaction.data
        id = interaction.id
        token = interaction.token
        if data["name"] == "say":
            json = {
                "type": 4,
                "data": {
                    "content": data["options"][0]["value"],
                }
            }
            async with bot.session.post(
                f"{bot.BASE_URL}/interactions/{id}/{token}/callback",
                json = json,
            ) as response:
                if not int(response.status/100) == 2:
                    print(f"HARUKA | Response of command 'say' returned status code {response.status}:")
                    print(await response.text())
        elif data["name"] == "sauce":
            results = await bot.get_sauce(data["options"][0]["value"])
            if not results:
                json = {
                    "type": 4,
                    "data": {
                        "content": "Cannot find the image sauce.",
                    }
                }
                async with bot.session.post(
                    f"{bot.BASE_URL}/interactions/{id}/{token}/callback",
                    json = json,
                ) as response:
                    if not int(response.status/100) == 2:
                        print(f"HARUKA | Response of command 'sauce' returned status code {response.status}:")
                        print(await response.text())
            else:
                embed = results[0].to_dict()
                embed["title"] = "Displaying the first result"
                embed["footer"] = {
                    "text": "For all results, consider using the text command"
                }
                json = {
                    "type": 4,
                    "data": {
                        "embeds": [embed],
                    }
                }
                async with bot.session.post(
                    f"{bot.BASE_URL}/interactions/{id}/{token}/callback",
                    json = json,
                ) as response:
                    if not int(response.status/100) == 2:
                        print(f"HARUKA | Response of command 'sauce' returned status code {response.status}:")
                        print(await response.text())
