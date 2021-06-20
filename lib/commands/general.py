import discord
from discord.ext import commands
from lib.settings import *

@bot.command()
async def addbot(cmd):
    em = discord.Embed(title="Invite me to your server", description="Invitation link: https://discord.com/oauth2/authorize?client_id=848178172536946708&scope=bot", color=0x2ECC71)
    em.set_thumbnail(url=bot.user.avatar_url)
    await cmd.send(embed=em)


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def info(cmd, *, user: discord.User = None):
    if user == None:
        user = cmd.author
    info_em = discord.Embed(
        title=f"{user} Info",
        description=f"**Name** {user.name}\n**Ping** <@!{user.id}>\n**ID** {user.id}",
        color=0x2ECC71,
    )
    if str(cmd.message.channel.type) == "private":
        info_em.set_footer(text="From private channel")
    elif str(cmd.message.channel.type) == "text":
        info_em.set_footer(text=f"From {cmd.message.guild}")
    await cmd.send(embed=info_em)


@info.error
async def info_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check yout input again.")


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def prefix(cmd, *, arg = None):
    db = bot.get_channel(int(CHANNEL_ID))
    if arg == None:
        if str(cmd.message.channel.type) == "private":
            id = str(cmd.message.channel.id)
        if str(cmd.message.channel.type) == "text":
            id = str(cmd.message.guild.id)
        async for message in db.history(limit=200):
            if message.author == bot.user and message.content.split("=")[0] == id:
                await cmd.send(
                    "My current prefix is: {0}".format(message.content.split("=")[1])
                )
        return
    if "=" in arg:
        await cmd.send("Prefixes cannot contain `=`")
        return
    else:
        if str(cmd.message.channel.type) == "private":
            id = cmd.message.channel.id
        elif str(cmd.message.channel.type) == "text":
            id = cmd.message.guild.id
        else:
            await cmd.send("Unsupported channel")
            return
        async for message in db.history(limit=200):
            if message.author == bot.user and message.content.split("=")[0] == str(id):
                await message.edit(content=f"{id}={arg}")
                await cmd.send(f"Prefix has been set to `{arg}`")
                break


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def say(cmd, *, arg):
    await cmd.send(arg)


@bot.command(aliases=["ava"])
@commands.cooldown(1, 2, commands.BucketType.user)
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
@commands.cooldown(1, 2, commands.BucketType.user)
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