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
        file = discord.File("./log.txt")
        await bot.get_user(ME).send("Bot has just started. This is the report.", file = file)
        print(f"HARUKA | Logged in as {bot.user} | Running in {len(bot.guilds)} servers.")


    # Run the bot
    bot.run(TOKEN)