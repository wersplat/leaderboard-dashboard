import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import sqlite3
from flask import Flask, render_template, g
from dotenv import load_dotenv

load_dotenv()

print(sys.executable)

app = Flask(__name__)
DATABASE = os.getenv('DATABASE', '/tmp/leaderboard.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        with app.app_context():
            with open('schema.sql', 'r') as f:
                db.cursor().executescript(f.read())
            # Check if the teams table is empty
            cur = db.cursor()
            cur.execute("SELECT COUNT(*) FROM teams")
            count = cur.fetchone()[0]
            if count == 0:
                # Insert sample data
                cur.execute(
                    "INSERT INTO teams (team_name, wins, losses) VALUES "
                    "('Team A', 10, 5)"
                )
                cur.execute(
                    "INSERT INTO teams (team_name, wins, losses) VALUES "
                    "('Team B', 7, 8)"
                )
                cur.execute(
                    "INSERT INTO teams (team_name, wins, losses) VALUES "
                    "('Team C', 12, 3)"
                )
                cur.execute(
                    "INSERT INTO teams (team_name, wins, losses) VALUES "
                    "('Team D', 5, 10)"
                )
                db.commit()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def leaderboard():
    cur = get_db().cursor()
    cur.execute("SELECT team_name, wins, losses FROM teams ORDER BY wins DESC")
    rows = cur.fetchall()
    return render_template('leaderboard.html', rows=rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
