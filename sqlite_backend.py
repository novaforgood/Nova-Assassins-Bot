import sqlite3


class SQLiteBackend:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        # Create players table
        self.conn.execute('''CREATE TABLE IF NOT EXISTS players (
                             uid INTEGER PRIMARY KEY,
                             score INTEGER DEFAULT 0,
                             lives INTEGER DEFAULT 3,
                             target_uid INTEGER,
                             FOREIGN KEY (target_uid) REFERENCES players(uid)
                             )''')

        # Create snipes table with image_url and message_id columns
        self.conn.execute('''CREATE TABLE IF NOT EXISTS snipes (
                             snipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
                             shooter_uid INTEGER NOT NULL,
                             target_uid INTEGER NOT NULL,
                             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                             success BOOLEAN NOT NULL,
                             image_url TEXT NOT NULL,
                             message_id INTEGER,
                             FOREIGN KEY (shooter_uid) REFERENCES players(uid),
                             FOREIGN KEY (target_uid) REFERENCES players(uid)
                             )''')

        self.conn.commit()

    def addPlayer(self, uid):
        # Adds a new player to the database
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO players (uid) VALUES (?)", (uid,))
                print(f"Player with UID {uid} added.")
        except sqlite3.IntegrityError:
            print(f"Player with UID {uid} already exists.")

    def uploadSnipe(self, shooter_uid, target_uid, image_url, success, message_id=None):
        # Uploads snipe data to the database
        with self.conn:
            cursor = self.conn.execute("INSERT INTO snipes (shooter_uid, target_uid, success, image_url, message_id) VALUES (?, ?, ?, ?, ?)",
                                       (shooter_uid, target_uid, success, image_url, message_id))
            snipe_id = cursor.lastrowid
            return snipe_id

    def getLeaderboard(self):
        # Returns a sorted list of players with their scores and lives
        with self.conn:
            cursor = self.conn.execute(
                "SELECT uid, score, lives FROM players ORDER BY score DESC, lives DESC")
            return cursor.fetchall()

    def getPlayer(self, uid):
        # Returns the info for one player
        with self.conn:
            cursor = self.conn.execute(
                "SELECT uid, score, lives, target_uid FROM players WHERE uid = ?", (uid,))
            return cursor.fetchone()

    def getSnipe(self, snipe_id):
        # Returns details of a specific snipe
        with self.conn:
            cursor = self.conn.execute(
                "SELECT * FROM snipes WHERE snipe_id = ?", (snipe_id,))
            return cursor.fetchone()

    def getSnipesOf(self, target_uid):
        # Returns all the snipes where the specified player was the target
        with self.conn:
            cursor = self.conn.execute(
                "SELECT * FROM snipes WHERE target_uid = ?", (target_uid,))
            return cursor.fetchall()

    def getSnipesBy(self, shooter_uid):
        # Returns all the snipes made by the specified player
        with self.conn:
            cursor = self.conn.execute(
                "SELECT * FROM snipes WHERE shooter_uid = ?", (shooter_uid,))
            return cursor.fetchall()

    def clearDatabase(self):
        # Clears the database
        with self.conn:
            self.conn.execute("DELETE FROM players")
            self.conn.execute("DELETE FROM snipes")
            self.conn.commit()

    def incrementScore(self, uid, increment=1):
        # Increment the score of a player
        with self.conn:
            self.conn.execute(
                "UPDATE players SET score = score + ? WHERE uid = ?", (increment, uid))

    def decrementScore(self, uid, decrement=1):
        # Decrement the score of a player
        with self.conn:
            self.conn.execute(
                "UPDATE players SET score = score - ? WHERE uid = ?", (decrement, uid))

    def incrementLives(self, uid, increment=1):
        # Increment the lives of a player
        with self.conn:
            self.conn.execute(
                "UPDATE players SET lives = lives + ? WHERE uid = ?", (increment, uid))

    def decrementLives(self, uid, decrement=1):
        # Decrement the lives of a player
        with self.conn:
            self.conn.execute(
                "UPDATE players SET lives = lives - ? WHERE uid = ?", (decrement, uid))

    def getPlayers(self):
        # Retrieves a list of all players with their details
        with self.conn:
            cursor = self.conn.execute(
                "SELECT uid, score, lives, target_uid FROM players")
            return cursor.fetchall()

    def setTarget(self, uid, target_uid):
        # Sets or updates the target of a player
        with self.conn:
            self.conn.execute(
                "UPDATE players SET target_uid = ? WHERE uid = ?", (target_uid, uid))

    def changeScore(self, uid, amount):
        # Changes the score of a player by a specified amount
        with self.conn:
            self.conn.execute(
                "UPDATE players SET score = score + ? WHERE uid = ?", (amount, uid))

    def getLatestSnipe(self, uid):
        # Retrieves the latest snipe associated with a player (target)
        with self.conn:
            cursor = self.conn.execute(
                "SELECT * FROM snipes WHERE target_uid = ? ORDER BY timestamp DESC LIMIT 1", (uid,))
            return cursor.fetchone()

    def close(self):
        # Closes the database connection
        self.conn.close()
