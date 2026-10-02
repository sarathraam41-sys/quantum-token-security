from src.banking.transactions import TransactionService
from src.banking.wallet import WalletService
from src.database.database import Database


def main():
    database = Database("test_transactions.db")

    wallets = WalletService(database)
    transactions = TransactionService(database)

    sender = "alice@upi"
    receiver = "bob@upi"

    print("Creating wallets...")

    wallets.ensure_wallet(sender)
    wallets.ensure_wallet(receiver)

    print("Alice balance before:", end=" ")

    alice = wallets.ensure_wallet(sender)
    print(alice["balance"])

    print("Bob balance before:", end=" ")

    bob = wallets.ensure_wallet(receiver)
    print(bob["balance"])

    print("\nTransferring ₹10,000...")

    transaction = transactions.transfer(
        sender,
        receiver,
        10_000,
    )

    print("Transaction:", transaction)

    print("\nBalances after transfer:")

    alice = wallets.ensure_wallet(sender)
    bob = wallets.ensure_wallet(receiver)

    print("Alice:", alice["balance"])
    print("Bob:", bob["balance"])

    print("\nTransaction history:")

    for item in transactions.list_transactions():
        print(item)

    if (
        alice["balance"] == 90_000
        and bob["balance"] == 110_000
    ):
        print("\nTransaction service test PASSED.")


if __name__ == "__main__":
    main()