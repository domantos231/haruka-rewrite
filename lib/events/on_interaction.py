import discord
from settings import *


@bot.event
async def on_interaction(interaction):
    """Execute slash commands"""
    interaction.data["id"] = interaction.id
    interaction.data["token"] = interaction.token
    await bot.process_slash_commands(interaction.data)