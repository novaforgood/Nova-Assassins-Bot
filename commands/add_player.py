import discord
from discord import app_commands
from discord.ext import commands
import helper
from datetime import datetime
from bot_config import PLAYER_ROLE

import sqlite_backend    # Database handling
db = sqlite_backend.SQLiteBackend("assassins.db")


@app_commands.command(name="addplayer", description="Add a player to the game")
async def add_player(ctx, player: discord.Member):

    # Ensure the player has the "W24Assassins" role
    hasRole = False
    for role in player.roles:
        if role.name == PLAYER_ROLE:
            hasRole = True
            break
    if not hasRole:
        await ctx.response.send_message(f"That player does not have the {PLAYER_ROLE} role.", allowed_mentions=discord.AllowedMentions.none())
        return

    # Ensure the player is not already in the game
    if db.getPlayer(player.id) is not None:
        await ctx.response.send_message("That player is already in the game.", allowed_mentions=discord.AllowedMentions.none())

    # Add the player to the database
    db.addPlayer(player.id)
    await ctx.response.send_message(f"Added {helper.uidToDisplayString(db, player.id)} to the game!", allowed_mentions=discord.AllowedMentions.all())
