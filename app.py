from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO

from src.banking.transactions import TransactionService
from src.banking.wallet import WalletService
from src.database.database import Database
from src.quantum.token import create_quantum_token
from src.quantum.verification import verify_token


app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
)

database = Database()

wallets = WalletService(database)

transactions = TransactionService(database)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.post("/login")
def do_login():
    data = request.get_json(force=True)

    upi = str(
        data.get("upi", "")
    ).strip()

    if not upi:
        return jsonify(
            {"error": "UPI identifier is required"}
        ), 400

    wallet = wallets.ensure_wallet(upi)

    return jsonify(
        {
            "status": "ok",
            "upi": wallet["upi"],
        }
    )


@app.post("/balance")
def balance():
    data = request.get_json(force=True)

    upi = str(
        data.get("upi", "")
    ).strip()

    if not upi:
        return jsonify(
            {"error": "UPI identifier is required"}
        ), 400

    wallet = wallets.ensure_wallet(upi)

    return jsonify(
        {
            "balance": wallet["balance"],
            "collapsed": wallet["collapsed"],
        }
    )


@app.post("/transfer")
def transfer():
    data = request.get_json(force=True)

    sender = str(
        data.get("sender", "")
    ).strip()

    receiver = str(
        data.get("receiver", "")
    ).strip()

    try:
        amount = int(
            data.get("amount", 0)
        )
    except (TypeError, ValueError):
        return jsonify(
            {"error": "Amount must be an integer"}
        ), 400

    if not sender or not receiver:
        return jsonify(
            {
                "error":
                "Sender and receiver are required"
            }
        ), 400

    if amount <= 0:
        return jsonify(
            {
                "error":
                "Amount must be greater than zero"
            }
        ), 400

    try:
        transaction = transactions.transfer(
            sender,
            receiver,
            amount,
        )

    except ValueError as error:
        return jsonify(
            {"error": str(error)}
        ), 400

    socketio.emit(
        "tx",
        transaction,
    )

    return jsonify(
        {
            "status": "success",
            "transaction": transaction,
        }
    )


@app.get("/admin_logs")
def admin_logs():
    return jsonify(
        transactions.list_transactions()
    )


@app.post("/admin_spy")
def admin_spy():
    data = request.get_json(force=True)

    upi = str(
        data.get("upi", "")
    ).strip()

    if not upi:
        return jsonify(
            {"error": "UPI identifier is required"}
        ), 400

    wallet = wallets.ensure_wallet(upi)

    if wallet["collapsed"]:
        return jsonify(
            {
                "collapse": True,
                "status":
                "Quantum token already collapsed",
            }
        )

    wallets.set_collapsed(
        upi,
        True,
    )

    socketio.emit(
        "collapse_token",
        {"upi": upi},
    )

    return jsonify(
        {
            "collapse": True,
            "status":
            "Quantum Token Collapsed",
        }
    )


@app.post("/verify_token")
def verify():
    data = request.get_json(force=True)

    upi = str(
        data.get("upi", "")
    ).strip()

    malicious = bool(
        data.get("malicious", False)
    )

    if not upi:
        return jsonify(
            {"error": "UPI identifier is required"}
        ), 400

    wallet = wallets.ensure_wallet(upi)

    result = verify_token(
        wallet["token"],
        malicious=malicious,
    )

    return jsonify(result)


@app.post("/reissue_token")
def reissue():
    data = request.get_json(force=True)

    upi = str(
        data.get("upi", "")
    ).strip()

    if not upi:
        return jsonify(
            {"error": "UPI identifier is required"}
        ), 400

    wallet = wallets.ensure_wallet(upi)

    if not wallet["collapsed"]:
        return jsonify(
            {"status": "still_valid"}
        )

    new_token = create_quantum_token()

    wallets.replace_token(
        upi,
        new_token,
    )

    socketio.emit(
        "new_token",
        {"upi": upi},
    )

    return jsonify(
        {"status": "new_token_issued"}
    )


if __name__ == "__main__":
    database.init_db()

    print()
    print("QuantumBank Security Server")
    print("----------------------------")
    print(
        "User Dashboard -> "
        "http://localhost:5000"
    )
    print(
        "Admin Console  -> "
        "http://localhost:5000/admin"
    )
    print()

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
    )