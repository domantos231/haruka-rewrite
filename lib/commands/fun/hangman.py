import asyncio
import aiohttp
import discord
from bs4 import BeautifulSoup as bs
from discord.ext import commands
from random import choice
from settings import *


HangmanInProgress = {}


class HangmanProgress:
    def __init__(self, word, guessed, life):
        self._word = word
        self.guessed = guessed
        self.life = life
    

    @property
    def word(self):
        return self._word


@bot.command(
    name = "hangman",
    description = "Play hangman game",
    usage = "hangman <initial number of lives | default: 5>",
)
async def _hangman(cmd, n: int = 5):
    if n < 1:
        await cmd.send("Initial number of lives must be greater than 0.")
        return
    if n > 15:
        await cmd.send("Initial number of lives must not exceed 15.")
        return
    if cmd.author.id not in HangmanInProgress:
        word = choice(bot.wordlist)
        while len(word) < 3:
            word = choice(bot.wordlist)
        length = len(word)
        HangmanInProgress[cmd.author.id] = HangmanProgress(word, [], n)
        em = discord.Embed(
            title="Hangman Game",
            description="".join("-" for i in range(length)) + "\nSend any character or send the entire word to guess!",
            color=0x2ECC71
        )
        em.set_author(name=f"{cmd.author.name} started Hangman Game!", icon_url=cmd.author.avatar_url)
        em.set_footer(text=f"💖 {n} left")
        msg = await cmd.send(embed=em)


        def check(message):
            return message.author.id == cmd.author.id and message.channel.id == cmd.channel.id
        

        while cmd.author.id in HangmanInProgress:
            game = HangmanInProgress[cmd.author.id]
            display = ""
            try:
                message = await bot.wait_for("message", check=check, timeout=300.0)
            except asyncio.TimeoutError:
                await cmd.send(f"<@!{cmd.author.id}> timed out for Hangman Game! The answer is **{word}**")
                del HangmanInProgress[cmd.author.id]
                return
            else:
                await msg.delete()
                guess = message.content.lower().replace(" ", "")
                if len(guess) == 1 and guess in word:
                    game.guessed.append(guess)
                    for char in word:
                        if char not in game.guessed:
                            display += "-"
                        else:
                            display += char
                    em = discord.Embed(
                        title="Hangman Game",
                        description=f"{display}\nSend any character or send the entire word to guess!",
                        color=0x2ECC71
                    )
                    em.set_author(name=f"{cmd.author.name} guessed 1 more character!", icon_url=cmd.author.avatar_url)
                    em.set_footer(text=f"💖 {game.life} left")
                    msg = await message.channel.send(embed=em)
                elif len(guess) == 1:
                    game.life -= 1
                    for char in word:
                        if char not in game.guessed:
                            display += "-"
                        else:
                            display += char
                    em = discord.Embed(
                        title="Hangman Game",
                        description=f"{display}\nSend any character or send the entire word to guess!",
                        color=0x2ECC71
                    )
                    em.set_author(name=f"{cmd.author.name} guessed incorrectly!", icon_url=cmd.author.avatar_url)
                    em.set_footer(text=f"💖 {game.life} left")
                    msg = await message.channel.send(embed=em)
                elif guess == game.word:
                    display = word
                    em = discord.Embed(
                        title="Hangman Game",
                        description=f"{display}\nSend any character or send the entire word to guess!",
                        color=0x2ECC71
                    )
                    em.set_author(name=f"{cmd.author.name} guessed the word!", icon_url=cmd.author.avatar_url)
                    em.set_footer(text=f"💖 {game.life} left")
                    msg = await message.channel.send(embed=em)
                else:
                    game.life -= 1
                    for char in word:
                        if char not in game.guessed:
                            display += "-"
                        else:
                            display += char
                    em = discord.Embed(
                        title="Hangman Game",
                        description=f"{display}\nSend any character or send the entire word to guess!",
                        color=0x2ECC71
                    )
                    em.set_author(name=f"{cmd.author.name} guessed incorrectly!", icon_url=cmd.author.avatar_url)
                    em.set_footer(text=f"💖 {game.life} left")
                    msg = await message.channel.send(embed=em)
                if game.life == 0:
                    await message.channel.send(f"<@!{cmd.author.id}> lost Hangman Game! The answer is **{word}**")
                    del HangmanInProgress[cmd.author.id]
                if display == word:
                    await message.channel.send(f"<@!{cmd.author.id}> won Hangman Game! ✨✨")
                    del HangmanInProgress[cmd.author.id]
