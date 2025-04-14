import os
import sys
import requests
import pandas as pd
from werkzeug.utils import secure_filename

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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    file_path = os.path.join('/tmp', filename)
    file.save(file_path)

    try:
        if filename.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif filename.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        else:
            return "Unsupported file format", 400

        db = get_db()
        for _, row in data.iterrows():
            db.execute('INSERT INTO leaderboard (team, wins, losses) VALUES (?, ?, ?)', (row['team'], row['wins'], row['losses']))
        db.commit()
        return "File uploaded and data inserted successfully", 200
    except Exception as e:
        return f"An error occurred: {e}", 500
    finally:
        os.remove(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
