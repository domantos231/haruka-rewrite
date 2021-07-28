import discord
from lib.settings import *


@bot.command(name="help")
async def _help(cmd):
    help_em = discord.Embed(
        title=f"{bot.user} command list",
        description=f"Ping <@!{bot.user.id}> for prefix",
        color=0x2ECC71,
    )
    help_em.set_thumbnail(url=bot.user.avatar_url)
    help_em.add_field(
        name="💬 General",
        value="```addbot, avatar, help, info, prefix, say, svinfo```",
        inline=False,
    )
    help_em.add_field(
        name="✨ Fun", value="```8ball, anime, hangman, math, sauce, search, roll```", inline=False
    )
    help_em.add_field(
        name="💵 Economy",
        value="```account, bank, battle, daily, gacha, gamble, pet```",
        inline=False,
    )
    help_em.add_field(
        name="🎶 Music",
        value="```pause, play, queue, remove, resume```",
        inline=False,
    )
    help_em.add_field(name="⚙️ Developer tools", value="```get, reset```", inline=False)
    await cmd.send(embed=help_em)
