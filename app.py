import os
import sys
import requests
import pandas as pd
from werkzeug.utils import secure_filename
import sqlite3
from flask import Flask, g, render_template, request

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

        # Validate required columns
        required_columns = {'team_name', 'wins', 'losses'}
        if not required_columns.issubset(data.columns):
            return f"Missing required columns: {required_columns - set(data.columns)}", 400

        db = get_db()
        for _, row in data.iterrows():
            db.execute(
                'INSERT INTO teams (team_name, wins, losses) VALUES (?, ?, ?)',
                (row['team_name'], row['wins'], row['losses'])
            )
        db.commit()
        return "File uploaded and data inserted successfully", 200
    except Exception as e:
        return f"An error occurred: {e}", 500
    finally:
        os.remove(file_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
