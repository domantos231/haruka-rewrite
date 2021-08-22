import discord
from discord.ext import commands
from settings import *


class HelpEmbed:
    def __init__(self, pref):
        self.pref = pref


    @property
    def display(self):
        embed = discord.Embed(
            title=self.title,
            description=f"{self.description}\nSyntax: `{self.pref}{self.syntax}`",
            color=0x2ECC71
        )
        embed.set_footer(text=f"Use {self.pref}help to get all commands!")
        return embed


class addbot(HelpEmbed):
    title = "addbot"
    description = "My invitation link: https://discord.com/api/oauth2/authorize?client_id=848178172536946708&permissions=2151018320&scope=bot"
    syntax = "addbot"


class avatar(HelpEmbed):
    title = "avatar"
    description = "Get the avatar from a Discord user."
    syntax = "avatar|ava <user|None>"


class help_embed(HelpEmbed):
    title = "help"
    description = "Display all commands or help for a specific command."
    syntax = "help <command|None>"


class info(HelpEmbed):
    title = "info"
    description = "Display a user's information"
    syntax = "info <user|None>"


class prefix(HelpEmbed):
    title = "prefix"
    description = "See the current prefix or change the bot's prefix (you must have administrator permission)"
    syntax = "prefix <new prefix|None>"


class say(HelpEmbed):
    title = "say"
    description = "Make the bot says something"
    syntax = "say <anything>"


class svinfo(HelpEmbed):
    title = "svinfo"
    description = "Display server information"
    syntax = "svinfo"


class _8ball(HelpEmbed):
    title = "8ball"
    description = "Ask the 8ball some questions"
    syntax = "8ball <question>"


class anime(HelpEmbed):
    title = "anime"
    description = "Search for an anime from MyAnimeList"
    syntax = "anime <search query>"


class hangman(HelpEmbed):
    title = "hangman"
    description = "Play a hangman game"
    syntax = "hangman <initial number of lives|None>"


class sauce(HelpEmbed):
    title = "sauce"
    description = "Search for the source of images (from pixiv, for example)"
    syntax = "sauce <URL to image or attachment>"


class search(HelpEmbed):
    title = "search"
    description = "Search Urban Dictionary for a term"
    syntax = "search <search query>"


class roll(HelpEmbed):
    title = "roll"
    description = "Generate a random number between <i> and <j>"
    syntax = "roll <i> <j>"


class account(HelpEmbed):
    title = "account"
    description = "See your or another user's economy account"
    syntax = "account|acc <user|None>"


class bank(HelpEmbed):
    title = "bank"
    description = "Visit the bank or deposit/withdraw money"
    syntax = "bank <deposit|withdraw|None> <amount|None>"


class battle(HelpEmbed):
    title = "battle"
    description = "Battle with another user"
    syntax = "battle <user>"


class daily(HelpEmbed):
    title = "daily"
    description = "Claim daily reward"
    syntax = "daily"


class gacha(HelpEmbed):
    title = "gacha"
    description = "Enjoy the gacha hell.\n-----------------\nRate up details:\n**COMMON** `50%`\n**RARE** `30.33%`\n**EPIC** `15.33%`\n**LEGENDARY** `4.33%`\n**????** `0.01%`"
    syntax = "gacha <number of rolls|None>"


class dice(HelpEmbed):
    title = "dice"
    description = "Roll a dice and compete with the bot"
    syntax = "dice <amount>"


class pet(HelpEmbed):
    title = "pet"
    description = "See your or another user's pets"
    syntax = "pet <user|None>"


class cry(HelpEmbed):
    title = "cry"
    description = "When you wants to cry a lot..."
    syntax = "cry"


class girl(HelpEmbed):
    title = "girl"
    description = "Send you a 2D animated girl. Really, go get a real girlfriend!"
    syntax = "girl"


class hug(HelpEmbed):
    title = "hug"
    description = "Hug someone"
    syntax = "hug <user>"


class kiss(HelpEmbed):
    title = "kiss"
    description = "Kiss someone"
    syntax = "kiss <user>"


class loli(HelpEmbed):
    title = "loli"
    description = "Send you a 2D loli. There's also a chance that you will be arrested by the FBI."
    syntax = "loli"


class punch(HelpEmbed):
    title = "punch"
    description = "Punch someone"
    syntax = "punch <user>"


class pause(HelpEmbed):
    title = "pause"
    description = "Pause the playing audio"
    syntax = "pause"


class play(HelpEmbed):
    title = "play"
    description = "Start playing music in the queue"
    syntax = "play <loop|verbose|None>"


class queue(HelpEmbed):
    title = "queue"
    description = "View the current music queue"
    syntax = "queue"


class remove(HelpEmbed):
    title = "remove"
    description = "Remove a track from queue"
    syntax = "remove <index|None>"


class resume(HelpEmbed):
    title = "resume"
    description = "Resume the paused audio"
    syntax = "resume"


class stop(HelpEmbed):
    title = "stop"
    description = "Stop the playing audio and disconnect from voice channel"
    syntax = "stop"


class add(HelpEmbed):
    title = "add"
    description = "Add a song to queue"
    syntax = "add <searching query>"


class card(HelpEmbed):
    title = "card"
    description = "Draw from 1 or 6 cards"
    syntax = "card <integer>"


command_list = ["addbot", "avatar", "help", "info", "prefix", "say", "svinfo", "8ball", "anime", "hangman", "sauce", "search", "roll", "account", "bank", "battle", "daily", "gacha", "dice", "pet", "cry", "girl", "hug", "kiss", "loli", "punch", "pause", "play", "queue", "remove", "resume", "stop", "add", "card"]
embed_class_list = HelpEmbed.__subclasses__()


@bot.command(name="help")
async def _help(cmd, help_request = None):
    if help_request is None:
        help_em = discord.Embed(
            title=f"{bot.user} command list",
            description=f"Ping <@!{bot.user.id}> for prefix.\nTo get help on a command, type `{cmd.prefix}help <command>`",
            color=0x2ECC71,
        )
        help_em.set_thumbnail(url=bot.user.avatar_url)
        help_em.add_field(
            name="💬 General",
            value="```addbot, avatar, help, info, prefix, say, svinfo```",
            inline=False,
        )
        help_em.add_field(
            name="✨ Fun", value="```8ball, anime, card, hangman, sauce, search, roll```", inline=False
        )
        help_em.add_field(
            name="💵 Economy",
            value="```account, bank, battle, daily, dice, gacha, pet```",
            inline=False,
        )
        help_em.add_field(
            name="🖼️ GIFs",
            value="```cry, girl, hug, kiss, loli, punch```",
            inline=False,
        )
        help_em.add_field(
            name="🎶 Music",
            value="```add, pause, play, queue, remove, resume, stop```",
            inline=False,
        )
        await cmd.send(embed=help_em)
    elif help_request.lower() in command_list:
        index = command_list.index(help_request.lower())
        await cmd.send(embed=embed_class_list[index](cmd.prefix).display)
    else:
        await cmd.send(f"No help found for `{help_request.lower()}`. Please do not use command aliases when trying to get help.")
        


@_help.error
async def help_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")
