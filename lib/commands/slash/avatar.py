from settings import *


json = {
    "name": "avatar",
    "type": 1,
    "description": "Find the image source with saucenao",
    "options": [{
        "name": "user",
        "description": "The target user to get the avatar from",
        "type": 6,
        "required": True,
    }]
}


@bot.slash(json)
async def avatar_(data):
    id = data["id"]
    token = data["token"]
    user_id = int(list(data["resolved"]["users"].keys())[0])
    user = bot.get_user(user_id)
    if user:
        embed = {
            "author": {
                "name": f"This is {user.name}'s avatar",
                "icon_url": bot.user.avatar.url,
            },
            "image": {
                "url": user.avatar.url,
            },
            "color": 0x2ECC71,
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
                print(f"HARUKA | Response of command 'avatar' returned status code {response.status}:")
                print(await response.text())
    else:
        json = {
            "type": 4,
            "data": {
                "content": "Cannot find this user.",
            }
        }
        async with bot.session.post(
            f"{bot.BASE_URL}/interactions/{id}/{token}/callback",
            json = json,
        ) as response:
            if not int(response.status/100) == 2:
                print(f"HARUKA | Response of command 'avatar' returned status code {response.status}:")
                print(await response.text())
