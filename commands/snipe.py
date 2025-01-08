import discord
from discord import app_commands
from discord.ext import commands
import helper
from datetime import datetime

import sqlite_backend    # Database handling
db = sqlite_backend.SQLiteBackend("assassins.db")


@app_commands.command(name="snipe", description="Upload a picture and tag a person")
async def snipe(ctx, target: discord.Member, image: discord.Attachment):

    # # Ensure the user is not trying to snipe themselves
    if ctx.user.id == target.id:
        await ctx.response.send_message("You cannot snipe yourself.", allowed_mentions=discord.AllowedMentions.none())
        return

    # # Ensure the user is not trying to snipe a bot
    if target.bot:
        await ctx.response.send_message("You cannot snipe a bot.", allowed_mentions=discord.AllowedMentions.none())
        return

    # # Ensure the target is playing the game
    if db.getPlayer(target.id) is None:
        await ctx.response.send_message("That target is not playing the game.", allowed_mentions=discord.AllowedMentions.none())
        return

    # # Process the snipe if there is an attachment
    if image is not None:
        link = image.url
        image_url = link.split("?")[0]
        shooter_uid = ctx.user.id
        target_uid = target.id
        image_url = link

        message = ""
        # get the current time using the library datetime
        timestamp = datetime.utcnow()

        # Ensure the target isn't getting farmed
        lastSnipeOfTarget = db.getLatestSnipe(target_uid)
        if lastSnipeOfTarget is not None:

            lastSnipeTimestamp = datetime.fromisoformat(lastSnipeOfTarget[3])
            timeDifference = (timestamp - lastSnipeTimestamp).seconds

            # if it has been less than 5 minutes since the last snipe of the target don't allow the snipe
            if timeDifference < 300:
                await ctx.response.send_message(f"{helper.uidToDisplayString(db, target_uid)} was sniped too recently! We don't want to farm them 🐮.", allowed_mentions=discord.AllowedMentions.none())
                return

            # if it has been less than 2 hours and the shooter is the same don't allow the snipe
            # TODO: check all snipes of the target, not just the last one 💀
            if timeDifference < 7200 and lastSnipeOfTarget[1] == shooter_uid:
                await ctx.response.send_message("You can't snipe the same person again so soon!", allowed_mentions=discord.AllowedMentions.none())
                return

        # Upload the snipe to the database
        snipe_id = db.uploadSnipe(
            shooter_uid, target_uid, image_url, success=True)

        # # Update the shooter's score
        # db.changeScore(shooter_uid, 100)

        # Get the shooter
        shooter = db.getPlayer(shooter_uid)
        target = db.getPlayer(target_uid)

        # check if the shooter's target is the target
        if shooter[3] == target_uid and target[2] > 0:

            db.changeScore(shooter_uid, 5)

            # db.decrementLives(target_uid) # TODO: bring back later
            # remove the target from the shooter
            db.setTarget(shooter_uid, None)

            message += f"{helper.uidToDisplayString(db, shooter_uid)} sniped their target {helper.uidToDisplayString(db, target_uid)}!"

            target = db.getPlayer(target_uid)
            if target[2] == 0:
                message += f"\n{helper.uidToDisplayString(db, target_uid)} is dead!"
        else:
            db.changeScore(shooter_uid, 1)
            message += f"{helper.uidToDisplayString(db, shooter_uid)} sniped {helper.uidToDisplayString(db, target_uid)}!"

        # message += "\n\n"
        # message += image_url

        # Download the image and send it as a file
        file = await image.to_file()
        await ctx.response.send_message(message, file=file, allowed_mentions=discord.AllowedMentions.none())

        # # download the image
        # im

        # await ctx.response.send_message(message, allowed_mentions=discord.AllowedMentions.none())

    else:
        await ctx.response.send_message("You must attach an image to snipe.", allowed_mentions=discord.AllowedMentions.all())
