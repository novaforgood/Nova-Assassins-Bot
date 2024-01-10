import discord
from discord import app_commands
from discord.ext import commands


@app_commands.command(name="helloworld", description="Say hello world!")
async def helloworld(ctx, target: discord.Member):
    ctx.respond("Hello world!")
