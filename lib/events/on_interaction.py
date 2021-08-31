import discord
from settings import *


@bot.event
async def on_interaction(interaction):
    """Execute slash commands"""
    await bot.process_slash_commands(interaction)