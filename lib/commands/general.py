import discord
from discord.ext import commands
from settings import *

@bot.command()
async def addbot(cmd):
    em = discord.Embed(
        title="Invite me to your server",
        description="My invitation link: https://discord.com/api/oauth2/authorize?client_id=848178172536946708&permissions=2151018320&scope=bot",
        color=0x2ECC71
    )
    em.set_thumbnail(url=bot.user.avatar_url)
    await cmd.send(embed=em)


@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def info(cmd, *, user: discord.User = None):
    if user == None:
        user = cmd.author
    info_em = discord.Embed(
        title=f"{user} Info",
        description=f"**Name** {user.name}\n**Ping** <@!{user.id}>\n**ID** {user.id}",
        color=0x2ECC71,
    )
    info_em.set_thumbnail(url=user.avatar_url)
    if str(cmd.message.channel.type) == "private":
        info_em.set_footer(text="From private channel")
    elif str(cmd.message.channel.type) == "text":
        info_em.set_footer(text=f"From {cmd.message.guild}")
    await cmd.send(embed=info_em)


@info.error
async def info_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")


@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def prefix(cmd, *, arg = None):
    id = cmd.guild.id
    if arg == None:
        await cmd.send("Please specify a prefix to change to!")
    else:
        cur.execute(f"""
        UPDATE prefix
        SET pref = '{arg}'
        WHERE id = '{id}';
        """)
        conn.commit()
        await cmd.send(f"Prefix has been set to `{arg}`")


@prefix.error
async def prefix_error(cmd, error):
    await cmd.send("You can ping me to get prefix anytime! Changing prefix in a server requires `Administrator` permission.")


@bot.command()
async def say(cmd, *, arg):
    await cmd.send(arg)


@bot.command(aliases=["ava"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def avatar(cmd, *, user: discord.User = None):
    if user == None:
        user = cmd.author
    ava_em = discord.Embed(
        description=f"This is <@!{user.id}>'s avatar:", color=0x2ECC71
    )
    ava_em.set_image(url=user.avatar_url)
    await cmd.send(embed=ava_em)


@avatar.error
async def avatar_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")


@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def svinfo(cmd):
    if str(cmd.message.channel.type) == "text":
        sv_em = discord.Embed(
            title="Server info",
            description="**Server name** "
            + str(cmd.message.guild)
            + "\n**Server ID** "
            + str(cmd.message.guild.id)
            + "\n**Member count** "
            + str(cmd.message.guild.member_count),
            color=0x2ECC71,
        )
        sv_em.set_thumbnail(url=cmd.guild.icon_url)
        await cmd.send(embed=sv_em)
    elif str(cmd.message.channel.type) == "private":
        await cmd.send(
            embed=discord.Embed(
                title="Server info",
                description=f"Private channel\n**Channel ID** {cmd.message.channel.id}",
                color=0x2ECC71,
            )
        )
    else:
        await cmd.send("Unsupported channel")
