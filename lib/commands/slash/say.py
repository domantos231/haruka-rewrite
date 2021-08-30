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
async def say_(data):
    id = data["id"]
    token = data["token"]
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
