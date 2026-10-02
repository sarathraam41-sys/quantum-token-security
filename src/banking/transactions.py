from src.banking.wallet import DEFAULT_BALANCE
from src.database.database import Database
from src.quantum.token import create_quantum_token


class TransactionService:
    """Transaction management for the QuantumBank demonstration."""

    def __init__(self, database: Database):
        self.database = database

    def _ensure_wallet(
        self,
        connection,
        upi: str,
    ):
        """Create a wallet if it does not already exist."""

        row = connection.execute(
            """
            SELECT *
            FROM users
            WHERE upi = ?
            """,
            (upi,),
        ).fetchone()

        if row is None:
            connection.execute(
                """
                INSERT INTO users
                (upi, balance, token, collapsed)
                VALUES (?, ?, ?, 0)
                """,
                (
                    upi,
                    DEFAULT_BALANCE,
                    self.database.serialize_token(
                        create_quantum_token()
                    ),
                ),
            )

    def transfer(
        self,
        sender: str,
        receiver: str,
        amount: int,
    ) -> dict:
        """Transfer funds between two wallets."""

        if sender == receiver:
            raise ValueError(
                "Sender and receiver must be different"
            )

        if amount <= 0:
            raise ValueError(
                "Amount must be greater than zero"
            )

        with self.database.connect() as connection:

            self._ensure_wallet(
                connection,
                sender,
            )

            self._ensure_wallet(
                connection,
                receiver,
            )

            sender_row = connection.execute(
                """
                SELECT balance
                FROM users
                WHERE upi = ?
                """,
                (sender,),
            ).fetchone()

            if sender_row["balance"] < amount:
                raise ValueError(
                    "Insufficient balance"
                )

            connection.execute(
                """
                UPDATE users
                SET balance = balance - ?
                WHERE upi = ?
                """,
                (
                    amount,
                    sender,
                ),
            )

            connection.execute(
                """
                UPDATE users
                SET balance = balance + ?
                WHERE upi = ?
                """,
                (
                    amount,
                    receiver,
                ),
            )

            cursor = connection.execute(
                """
                INSERT INTO transactions
                (sender, receiver, amount)
                VALUES (?, ?, ?)
                """,
                (
                    sender,
                    receiver,
                    amount,
                ),
            )

            connection.commit()

            return {
                "id": cursor.lastrowid,
                "from": sender,
                "to": receiver,
                "amount": amount,
            }

    def list_transactions(self) -> list[dict]:
        """Return transactions from newest to oldest."""

        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    sender,
                    receiver,
                    amount,
                    created_at
                FROM transactions
                ORDER BY id DESC
                """
            ).fetchall()

        return [
            {
                "id": row["id"],
                "from": row["sender"],
                "to": row["receiver"],
                "amount": row["amount"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]