import sqlite_backend
import random


def assignTargets(db: sqlite_backend.SQLiteBackend):
    # Get the list of players
    players = db.getPlayers()

    # Shuffle the list of players
    random.shuffle(players)

    # Remove the dead players
    players = [player for player in players if player[2] > 0]

    # Assign targets
    for i in range(len(players)):
        # Get the player
        player = players[i]

        # Get the target
        target = players[(i+1) % len(players)]

        # Assign the target
        db.setTarget(player[0], target[0])


def doRound(db: sqlite_backend.SQLiteBackend, newGame=False):

    assignTargets(db)

    messages = []

    message = ""
    if newGame:
        message += "New game!\n\n"
    else:
        message += "New round!\n\n"
    message += "**📸 This round's targets! 🔫**\n"

    players = db.getPlayers()

    counter = 0
    for player in players:
        if player[2] == 0:
            continue
        counter += 1
        message += f"<@{player[0]}> ➡ <@{player[3]}>\n"
        if counter % 10 == 0:
            messages.append(message)
            message = ""

    if message != "":
        messages.append(message)
        message = ""

    # message += "\n"

    leaderboardMessages = getLeaderboardString(db)
    for lM in leaderboardMessages:
        messages.append(lM)

    return messages


def getLeaderboardString(db: sqlite_backend.SQLiteBackend):
    # Retrieve the leaderboard data from the database
    leaderboard_data = db.getLeaderboard()

    messages = []

    # Format the data for display
    message = "🏆 **Assassin's Leaderboard** 🏆\n"
    counter = 0
    for rank, (uid, score, lives) in enumerate(leaderboard_data, start=1):
        message += f"**{rank}.**\t{score}\t {uidToDisplayString(db, uid)}\n"
        counter += 1
        if counter % 10 == 0:
            messages.append(message)
            message = ""

    if message != "":
        messages.append(message)
        message = ""

    return messages


def uidToDisplayString(db, uid):
    hearts = "♥️" * db.getPlayer(uid)[2]
    if hearts == "":
        hearts = "💀"
    return f"<@{uid}>({hearts})"
