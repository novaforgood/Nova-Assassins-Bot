import discord
from discord import app_commands
from discord.ext import commands

import sqlite_backend  # Import the SQLite backend
from helper import getLeaderboardString

# Create an instance of the SQLiteBackend
db = sqlite_backend.SQLiteBackend("assassins.db")


@app_commands.command(name="leaderboard", description="View the game's leaderboard")
async def leaderboard(ctx):
    # Format the data for display
    messages = getLeaderboardString(db)
    # Send the formatted leaderboard as a response
    await ctx.response.send_message(messages[0], allowed_mentions=discord.AllowedMentions.none())
    for i in range(1, len(messages)):
        await ctx.channel.send(messages[i], allowed_mentions=discord.AllowedMentions.none())

    # await ctx.response.send_message(message, allowed_mentions=discord.AllowedMentions.none())

# Add additional functions if needed
