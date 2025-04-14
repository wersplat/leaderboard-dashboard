from flask import Flask, render_template, jsonify
from src.bot.leaderboard import Leaderboard

app = Flask(__name__)
leaderboard = Leaderboard()

@app.route('/')
def index():
    return render_template('leaderboard.html')

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    top_users = leaderboard.get_top_users(10)  # Fetch top 10 users
    return jsonify(top_users)

if __name__ == '__main__':
    app.run(debug=True)