import discord
from discord.ext import commands
from settings import *


class CustomHelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        help_em = discord.Embed(
            title=f"{bot.user} command list",
            description=f"Ping <@!{bot.user.id}> for prefix.\nTo get help on a command, type `{self.context.prefix}help <command>`",
            color=0x2ECC71,
        )
        help_em.set_thumbnail(url=bot.user.avatar.url)
        help_em.add_field(
            name="💬 General",
            value="```avatar, help, info, invite, ping, prefix, say, svinfo```",
            inline=False,
        )
        help_em.add_field(
            name="✨ Fun", value="```8ball, anime, card, hangman, roll, sauce, urban```", inline=False
        )
        help_em.add_field(
            name="💵 Economy",
            value="```4cards, account, bank, battle, blackjack, daily, dice, gacha, pet```",
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
        await self.context.send(embed=help_em)
    

    async def send_command_help(self, command: commands.Command):
        if not command.usage:
            command.usage = command.qualified_name
        em = discord.Embed(
            title = command.qualified_name,
            description = f"```\n{self.context.prefix}{command.usage}\n```\n**Description**\n{command.description}\n**Aliases**\n" + ", ".join(f"`{alias}`" for alias in command.aliases),
            color = 0x2ECC71,
        )
        em.set_author(name = f"{self.context.author.name}, this is an instruction for {command.qualified_name}!", icon_url = self.context.author.avatar.url)
        await self.context.send(embed = em)


    async def send_group_help(self, group: commands.Group):
        if not group.usage:
            group.usage = group.qualified_name
        em = discord.Embed(
            title = group.qualified_name,
            description = f"```\n{self.context.prefix}{group.usage}\n```\n**Description**\n{group.description}\n**Aliases**\n" + ", ".join(f"`{alias}`" for alias in group.aliases),
            color = 0x2ECC71,
        )
        em.set_author(name = f"{self.context.author.name}, this is an instruction for {group.qualified_name}!", icon_url = self.context.author.avatar.url)
        await self.context.send(embed = em)


bot.help_command = CustomHelpCommand()
