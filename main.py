import discord
from discord import app_commands

from bot_config import GUILD_ID, BOT_TOKEN, GUILD_IDS   # Configuration settings

from commands.snipe import snipe
from commands.hello import helloworld
from commands.leaderboard import leaderboard
from commands.init import initgame
from commands.next_round import nextround
from commands.add_player import add_player

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


tree.add_command(snipe, guilds=[discord.Object(id=GID) for GID in GUILD_IDS])
tree.add_command(helloworld, guilds=[
                 discord.Object(id=GID) for GID in GUILD_IDS])
tree.add_command(leaderboard, guilds=[
                 discord.Object(id=GID) for GID in GUILD_IDS])
tree.add_command(initgame, guilds=[
                 discord.Object(id=GID) for GID in GUILD_IDS])
tree.add_command(nextround,  guilds=[
                 discord.Object(id=GID) for GID in GUILD_IDS])
tree.add_command(add_player, guilds=[
                 discord.Object(id=GID) for GID in GUILD_IDS])


@client.event
async def on_ready():

    for GID in GUILD_IDS:
        await tree.sync(guild=discord.Object(id=GID))
    print("Ready!")

client.run(BOT_TOKEN)
