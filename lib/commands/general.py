import asyncio
import checks
import discord
from discord.ext import commands
from settings import *

@bot.command(
    name = "invite",
    description = "Get my invite link!",
)
async def _invite(cmd):
    em = discord.Embed(
        title = "Invite me to your server",
        description = r"My invitation link: https://discord.com/api/oauth2/authorize?client_id=848178172536946708&permissions=2151018320&scope=bot%20applications.commands",
        color = 0x2ECC71,
    )
    em.set_thumbnail(url=bot.user.avatar.url)
    await cmd.send(embed=em)


@bot.command(
    name = "info",
    description = "Get a user's information",
    usage = "info <user | default: yourself>"
)
@checks.channelCheck()
@commands.cooldown(1, 6, commands.BucketType.user)
async def _info(cmd, *, user: discord.Member = None):
    if user is None:
        user = cmd.author
    name = user.name.replace("*", r"\*")
    if user.nick:
        nick = user.nick.replace("*", r"\*")
    else:
        nick = user.name
    info_em = discord.Embed(
        title = f"{user} Information",
        description = f"**Name** {name}\n**Nickname** {nick}\n**Created** {(discord.utils.utcnow() - user.created_at).days} days ago\n**ID** {user.id}",
        color = 0x2ECC71,
    )
    info_em.add_field(
        name = "Joined server",
        value = f"{(discord.utils.utcnow() - user.joined_at).days} days ago"
    )
    info_em.add_field(
        name = "Roles",
        value = "\n".join(role.name.replace("*", r"\*") for role in user.roles[1:])
    )
    info_em.set_thumbnail(url = user.avatar.url)
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
    ava_em = discord.Embed(color = 0x2ECC71)
    ava_em.set_author(
        name = f"This is {user.name}'s avatar",
        icon_url = bot.user.avatar.url,
    )
    ava_em.set_image(url = user.avatar.url)
    await cmd.send(embed = ava_em)


@bot.command(
    name = "svinfo",
    description = "Retrieve information about a server",
)
@checks.channelCheck()
@commands.cooldown(1, 6, commands.BucketType.user)
async def _svinfo(cmd):
    guild = cmd.guild
    name = guild.name.replace("*", r"\*")
    sv_em = discord.Embed(
        title = "Server info",
        description = f"**Server name** {name}\n**Server ID** {guild.id}\n**Member count** {guild.member_count}",
        color = 0x2ECC71,
    )
    sv_em.add_field(
        name = "Server owner",
        value = guild.owner.name,
        inline = False,
    )
    sv_em.add_field(
        name = "Created",
        value = f"{(discord.utils.utcnow() - guild.created_at).days} days ago"
    )
    sv_em.add_field(
        name = "Text channels",
        value = len(guild.text_channels)
    )
    sv_em.add_field(
        name = "Voice channels",
        value = len(guild.voice_channels)
    )
    sv_em.add_field(
        name = "Emojis",
        value = len(guild.emojis)
    )
    sv_em.set_thumbnail(url = guild.icon.url)
    if guild.banner:
        sv_em.set_image(url = guild.banner.url)
    await cmd.send(embed = sv_em)


@bot.command(
    name = "emoji",
    description = "Show all emojis from the server",
)
@checks.channelCheck()
@commands.cooldown(1, 6, commands.BucketType.user)
async def _emoji(cmd):
    emojis = cmd.guild.emojis
    pages = 1 + int(len(emojis)/50)
    embeds = []
    for page in range(pages):
        em = discord.Embed(
            title = cmd.guild.name,
            description = "".join(f"<:{emoji.name}:{emoji.id}>" for emoji in emojis[page * 50:page * 50 + 50]),
            color = 0x2ECC71,
        )
        em.set_author(
            name = "These are the server's emojis!",
            icon_url = cmd.author.avatar.url,
        )
        em.set_thumbnail(url = cmd.guild.icon.url)
        em.set_footer(text = f"Showing page {page + 1}/{pages}")
        embeds.append(em)
    msg = await cmd.send(embed = embeds[0])
    for react in choices[:pages]:
        await msg.add_reaction(react)
    

    def check(reaction, user):
        return reaction.message.id == msg.id and str(reaction) in choices[:pages] and user.id == cmd.author.id
    

    async def active():
        while True:
            done, pending = await asyncio.wait(
                [bot.wait_for("reaction_add", check = check),
                bot.wait_for("reaction_remove", check = check)],
                return_when = asyncio.FIRST_COMPLETED,
            )
            reaction, user = done.pop().result()
            choice = choices.index(str(reaction))
            await msg.edit(embed = embeds[choice])
    

    try:
        await asyncio.wait_for(active(), timeout = 300.0)
    except asyncio.TimeoutError:
        await msg.clear_reactions()
        return


@bot.command(
    name = "ping",
    description = "Measures latency between a HEARTBEAT and a HEARTBEAT_ACK (from the bot to Discord WebSocket).",
)
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping(cmd):
    await cmd.send("🏓 **Pong!** | {:.2f} ms".format(1000 * bot.latency))