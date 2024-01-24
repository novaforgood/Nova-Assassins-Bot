import discord
from discord import app_commands
from discord.ext import commands
from helper import assignTargets, doRound


import sqlite_backend  # Import the SQLite backend

# Create an instance of the SQLiteBackend
db = sqlite_backend.SQLiteBackend("assassins.db")


@app_commands.command(name="initgame", description="Initialize the game")
async def initgame(ctx, password: str):

    if (password != "MEOW"):
        await ctx.response.send_message("Incorrect password.", allowed_mentions=discord.AllowedMentions.all())
        return
    # "I AM ABSOLUTELY CERTAIN THAT I WANT TO CLEAR THE DATABASE AND START A NEW GAME SLAY":

    db.clearDatabase()
    db._create_tables()

    # get a list of all the members in the server
    members = ctx.guild.members

    # add each member to the database
    for member in members:
        # if the member is a bot, skip them
        if member.bot:
            continue

        # check that the member has the "W24Assassins" role
        hasRole = False
        for role in member.roles:
            if role.name == "W24Assassins":
                hasRole = True
                break
        if not hasRole:
            continue

        db.addPlayer(member.id)

    messages = doRound(db, newGame=True)

    await ctx.response.send_message(messages[0], allowed_mentions=discord.AllowedMentions.all())
    for i in range(1, len(messages)):
        await ctx.channel.send(messages[i], allowed_mentions=discord.AllowedMentions.all())

# Add additional functions if needed
