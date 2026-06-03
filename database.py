import sqlite3
from datetime import datetime


class GestureDatabase:

    def __init__(self):

        self.conn = sqlite3.connect(
            "gesture_logs.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS gesture_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            gesture TEXT,
            value INTEGER
        )
        """)

        self.conn.commit()

    def log_action(
        self,
        gesture,
        value
    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.cursor.execute("""
        INSERT INTO gesture_logs(
            timestamp,
            gesture,
            value
        )
        VALUES(?,?,?)
        """, (
            timestamp,
            gesture,
            value
        ))

        self.conn.commit()

    def get_recent_logs(self, limit=20):

        self.cursor.execute("""
        SELECT *
        FROM gesture_logs
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    def clear_logs(self):

        self.cursor.execute("""
        DELETE FROM gesture_logs
        """)

        self.conn.commit()

    def close(self):

        self.conn.close()