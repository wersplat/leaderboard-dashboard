import os
import sys
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import sqlite3
from flask import Flask, render_template, g, request
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


# Load environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
RENDER_API_KEY = os.getenv('RENDER_API_KEY')
SERVICE_ID = os.getenv('SERVICE_ID')


@app.route('/stop-service', methods=['POST'])
def stop_service():
    # Verify the secret key
    if request.form.get('key') != SECRET_KEY:
        return "Forbidden", 403

    # Call Render API to stop the service
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}"
    }
    response = requests.post(f"https://api.render.com/v1/services/{SERVICE_ID}/stop", headers=headers)

    if response.status_code == 200:
        return "Service stopped successfully."
    else:
        return f"Failed to stop service: {response.status_code} - {response.text}", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
# Moved to dashboard/app.py in the new structure.
