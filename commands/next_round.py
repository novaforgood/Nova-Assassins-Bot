from discord import app_commands
from discord.ext import commands
import discord

import sqlite_backend  # Import the SQLite backend
from helper import doRound

# Create an instance of the SQLiteBackend
db = sqlite_backend.SQLiteBackend("assassins.db")


@app_commands.command(name="nextround", description="Start the next round and assign new targets")
async def nextround(ctx, password: str):

    if (password != "MEOW"):
        await ctx.response.send_message("Incorrect password.", allowed_mentions=discord.AllowedMentions.all())
        return
    # "I AM ABSOLUTELY CERTAIN THAT I WANT TO CLEAR THE DATABASE AND START A NEW GAME SLAY":

    messages = doRound(db, newGame=False)

    await ctx.response.send_message(messages[0], allowed_mentions=discord.AllowedMentions.all())
    for i in range(1, len(messages)):
        await ctx.channel.send(messages[i], allowed_mentions=discord.AllowedMentions.all())

# Add additional functions if needed
