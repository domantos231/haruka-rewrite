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
    em.set_thumbnail(url = bot.user.avatar.url)
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
    info_em = bot.user_info(user)
    info_em.set_footer(text = f"From {cmd.message.guild}")
    await cmd.send(embed=info_em)


@bot.command(
    name = "prefix",
    description = "Change the bot's prefix in this server.\nThis requires `Administrator` permission.",
    usage = "prefix <prefix>"
)
@commands.cooldown(1, 6, commands.BucketType.guild)
@checks.channelCheck()
@commands.has_permissions(administrator = True)
async def _prefix(cmd, *, arg = None):
    id = cmd.guild.id
    if arg == None:
        await cmd.send("Please specify a prefix to change to!")
    else:
        await bot.db.conn.execute(f"""
            UPDATE prefix
            SET pref = $1
            WHERE id = '{id}';
            """, str(arg)
        )
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
    if not user.avatar:
        return await cmd.send("This user hasn't uploaded an avatar yet.")
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
    sv_em = bot.server_info(cmd.guild)
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
            icon_url = cmd.author.avatar.url if cmd.author.avatar else discord.Embed.Empty,
        )
        em.set_thumbnail(url = cmd.guild.icon.url if cmd.guild.icon else discord.Embed.Empty)
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