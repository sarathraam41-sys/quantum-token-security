from src.database.database import Database
from src.quantum.token import create_quantum_token


DEFAULT_BALANCE = 100_000


class WalletService:
    """Wallet management for the QuantumBank demonstration."""

    def __init__(self, database: Database):
        self.database = database
        self.database.init_db()

    def ensure_wallet(self, upi: str) -> dict:
        """Create a wallet if it does not already exist."""

        with self.database.connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM users
                WHERE upi = ?
                """,
                (upi,),
            ).fetchone()

            if row is None:
                token = create_quantum_token()

                connection.execute(
                    """
                    INSERT INTO users
                    (upi, balance, token, collapsed)
                    VALUES (?, ?, ?, 0)
                    """,
                    (
                        upi,
                        DEFAULT_BALANCE,
                        self.database.serialize_token(token),
                    ),
                )

                connection.commit()

                return {
                    "upi": upi,
                    "balance": DEFAULT_BALANCE,
                    "token": token,
                    "collapsed": False,
                }

            return {
                "upi": row["upi"],
                "balance": row["balance"],
                "token": self.database.deserialize_token(
                    row["token"]
                ),
                "collapsed": bool(row["collapsed"]),
            }

    def set_collapsed(
        self,
        upi: str,
        collapsed: bool,
    ):
        """Update the application-level token collapse state."""

        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE users
                SET collapsed = ?
                WHERE upi = ?
                """,
                (
                    int(collapsed),
                    upi,
                ),
            )

            connection.commit()

    def replace_token(
        self,
        upi: str,
        token: dict,
    ):
        """Replace a collapsed token with a newly generated token."""

        with self.database.connect() as connection:
            connection.execute(
                """
                UPDATE users
                SET token = ?, collapsed = 0
                WHERE upi = ?
                """,
                (
                    self.database.serialize_token(token),
                    upi,
                ),
            )

            connection.commit()
            