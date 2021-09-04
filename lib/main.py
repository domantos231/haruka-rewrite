import discord


if __name__ == "__main__":
    from settings import *
    from events import *
    from commands import *


    @bot.event
    async def on_connect():
        print("HARUKA | Connected to Discord!")


    @bot.event
    async def on_ready():
        print(f"HARUKA | Logged in as {bot.user} | Running in {len(bot.guilds)} servers.")
        await bot.wait_until_ready()
        await bot.get_user(ME).send("I'm ready!")


    # Run the bot
    bot.run(TOKEN)