from lib.settings import *


@bot.command()
async def help(cmd):
    help_em = discord.Embed(
        title=f"{bot.user} command list",
        description=f"Ping <@!{bot.user.id}> for prefix",
        color=0x2ECC71,
    )
    help_em.add_field(
        name="General",
        value="```\naddbot, avatar, help, info, prefix, say, svinfo\n```",
        inline=False,
    )
    help_em.add_field(
        name="Fun", value="```\n8ball, anime, math, roll\n```", inline=False
    )
    help_em.add_field(
        name="Economy",
        value="```\naccount, battle, daily, gacha, gamble, pet\n```",
        inline=False,
    )
    help_em.add_field(name="Developer tools", value="```\nget\n```", inline=False)
    await cmd.send(embed=help_em)
