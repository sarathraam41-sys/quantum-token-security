import json
import sqlite3
from pathlib import Path


class Database:
    """SQLite persistence layer for the QuantumBank demonstration."""

    def __init__(self, path: str = "bank.db"):
        self.path = Path(path)

    def connect(self):
        connection = sqlite3.connect(
            self.path,
            check_same_thread=False,
        )

        connection.row_factory = sqlite3.Row

        return connection

    def init_db(self):
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    upi TEXT PRIMARY KEY,
                    balance INTEGER NOT NULL,
                    token TEXT NOT NULL,
                    collapsed INTEGER NOT NULL DEFAULT 0
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    receiver TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.commit()

    @staticmethod
    def serialize_token(token: dict) -> str:
        return json.dumps(token)

    @staticmethod
    def deserialize_token(token: str) -> dict:
        return json.loads(token)