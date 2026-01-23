from flask import Flask, request, jsonify

app = Flask(__name__)

# -----------------------------
# In-memory databases
# -----------------------------
players = {}
leaderboard = []

# Riddles based on difficulty
riddles = {
    1: [
        {"question": "What has to be broken before you can use it?", "answer": "egg"}
    ],
    2: [
        {"question": "I speak without a mouth and hear without ears. What am I?", "answer": "echo"}
    ],
    3: [
        {"question": "The more you take, the more you leave behind. What is it?", "answer": "footsteps"}
    ]
}

# -----------------------------
# Start Game (Boy starts running)
# -----------------------------
@app.route('/api/start-game', methods=['POST'])
def start_game():
    data = request.json
    username = data.get("username")

    players[username] = {
        "score": 0,
        "level": 1,
        "status": "running"
    }

    return jsonify({
        "message": "Game started. The boy is running!",
        "player": players[username]
    })


# -----------------------------
# Boy touches a snail → get riddle
# -----------------------------
@app.route('/api/snail-collision/<int:level>', methods=['GET'])
def snail_collision(level):
    riddle = riddles.get(level)

    if not riddle:
        return jsonify({"message": "No riddle available for this difficulty level"}), 404

    return jsonify({
        "event": "Boy touched a snail",
        "level": level,
        "question": riddle[0]["question"]
    })


# -----------------------------
# Check riddle answer
# -----------------------------
@app.route('/api/answer', methods=['POST'])
def check_answer():
    data = request.json
    username = data.get("username")
    level = data.get("level")
    answer = data.get("answer", "").lower()

    correct_answer = riddles[level][0]["answer"]

    if answer == correct_answer:
        players[username]["score"] += 10
        players[username]["level"] += 1

        return jsonify({
            "correct": True,
            "message": "Correct! The boy avoided the snail.",
            "new_score": players[username]["score"],
            "new_level": players[username]["level"]
        })
    else:
        players[username]["status"] = "game_over"

        return jsonify({
            "correct": False,
            "message": "Wrong answer! The boy was caught by the snail. Game over."
        })


# -----------------------------
# Save score after game over
# -----------------------------
@app.route('/api/score', methods=['POST'])
def save_score():
    data = request.json
    username = data.get("username")

    leaderboard.append({
        "username": username,
        "score": players[username]["score"]
    })

    leaderboard.sort(key=lambda x: x["score"], reverse=True)

    return jsonify({
        "message": "Score saved successfully"
    })


# -----------------------------
# Get leaderboard
# -----------------------------
@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    return jsonify(leaderboard[:5])


# -----------------------------
# Run server
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)