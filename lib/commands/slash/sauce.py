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
async def sauce_(data):
    results = await bot.get_sauce(data["options"][0]["value"])
    id = data["id"]
    token = data["token"]
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
