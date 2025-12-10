from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database for users
users = {
    "user1": {"phone": "254700111222", "balance": 5000},
    "user2": {"phone": "254700333444", "balance": 3000},
    "user3": {"phone": "254700777999", "balance": 6000},
    
}

# Check balance
@app.route('/balance/<username>', methods=['GET'])
def get_balance(username):
    user = users.get(username)
    if not user:
        return jsonify({"status": "failed", "message": "User not found"}), 404
    return jsonify({"status": "success", "balance": user["balance"]})

# Deposit money
@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    username = data.get("username")
    amount = data.get("amount")
    if username not in users:
        return jsonify({"status": "failed", "message": "User not found"}), 404
    if amount <= 0:
        return jsonify({"status": "failed", "message": "Invalid amount"}), 400
    users[username]["balance"] += amount
    return jsonify({"status": "success", "balance": users[username]["balance"]})

# Send money
@app.route('/send', methods=['POST'])
def send_money():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = data.get("amount")
    if sender not in users or receiver not in users:
        return jsonify({"status": "failed", "message": "Sender or receiver not found"}), 404
    if users[sender]["balance"] < amount:
        return jsonify({"status": "failed", "message": "Insufficient balance"}), 400
    users[sender]["balance"] -= amount
    users[receiver]["balance"] += amount
    return jsonify({
        "status": "success",
        "sender_balance": users[sender]["balance"],
        "receiver_balance": users[receiver]["balance"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

