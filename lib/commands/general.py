import discord
from discord.ext import commands
from settings import *

@bot.command(
    name = "invite",
    description = "Get my invite link!",
)
async def _invite(cmd):
    em = discord.Embed(
        title="Invite me to your server",
        description="My invitation link: https://discord.com/api/oauth2/authorize?client_id=848178172536946708&permissions=2151018320&scope=bot",
        color=0x2ECC71
    )
    em.set_thumbnail(url=bot.user.avatar_url)
    await cmd.send(embed=em)


@bot.command(
    name = "info",
    description = "Get a user's information",
    usage = "info <user | default: yourself>"
)
@commands.cooldown(1, 6, commands.BucketType.user)
async def _info(cmd, *, user: discord.Member = None):
    if user is None:
        user = cmd.author
    if isinstance(cmd.message.channel, discord.DMChannel):
        info_em = discord.Embed(
            title = f"{user} Information",
            description = f"**Name** {user.name}\n**Created at (UTC)** {user.created_at}\n**ID** {user.id}",
            color = 0x2ECC71,
        )
        info_em.set_thumbnail(url = user.avatar_url)
        info_em.set_footer(text="From private channel")
    elif isinstance(cmd.message.channel, discord.TextChannel):
        name = user.name.replace("*", "\*")
        if user.nick:
            nick = user.nick.replace("*", "\*")
        else:
            nick = user.name
        info_em = discord.Embed(
            title = f"{user} Information",
            description = f"**Name** {name}\n**Nickname** {nick}\n**Created at (UTC)** {user.created_at}\n**ID** {user.id}",
            color = 0x2ECC71,
        )
        info_em.add_field(
            name = "Joined server at (UTC)",
            value = user.joined_at
        )
        info_em.add_field(
            name = "Roles",
            value = "\n".join(role.name.replace("*", "\*") for role in user.roles[1:])
        )
        info_em.set_thumbnail(url = user.avatar_url)
        info_em.set_footer(text = f"From {cmd.message.guild}")
    await cmd.send(embed=info_em)


@bot.command(
    name = "prefix",
    description = "Change the bot's prefix in this server.\nThis requires `Administrator` permission.",
    usage = "prefix <prefix>"
)
@commands.cooldown(1, 6, commands.BucketType.guild)
@commands.has_permissions(administrator=True) # This also blocks prefix changing in DM channels
async def _prefix(cmd, *, arg = None):
    id = cmd.guild.id
    if arg == None:
        await cmd.send("Please specify a prefix to change to!")
    else:
        await bot.db.conn.execute(f"""
        UPDATE prefix
        SET pref = '{arg}'
        WHERE id = '{id}';
        """)
        await cmd.send(f"Prefix has been set to `{arg}`")


@bot.command(
    name = "say",
    description = "Make the bot says something",
    usage = "say <anything>"
)
async def _say(cmd, *, arg):
    await cmd.send(arg)


@bot.command(
    name = "avatar",
    aliases = ["ava"],
    description = "Get an avatar from a user",
    usage = "avatar <user | default: yourself>",
)
@commands.cooldown(1, 3, commands.BucketType.channel)
async def _avatar(cmd, *, user: discord.User = None):
    if user == None:
        user = cmd.author
    ava_em = discord.Embed(
        description=f"This is <@!{user.id}>'s avatar:", color=0x2ECC71
    )
    ava_em.set_image(url=user.avatar_url)
    await cmd.send(embed=ava_em)


@bot.command(
    name = "svinfo",
    description = "Retrieve information about a server",
)
@commands.cooldown(1, 6, commands.BucketType.channel)
async def _svinfo(cmd):
    if isinstance(cmd.message.channel, discord.TextChannel):
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
    elif isinstance(cmd.message.channel, discord.DMChannel):
        await cmd.send(
            embed=discord.Embed(
                title="Server info",
                description=f"Private channel\n**Channel ID** {cmd.message.channel.id}",
                color=0x2ECC71,
            )
        )
    else:
        await cmd.send("Unsupported channel")
