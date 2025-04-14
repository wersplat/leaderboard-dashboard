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
            else:
                # Remove sample data if real data exists
                cur.execute("DELETE FROM teams WHERE team_name IN ('Team A', 'Team B')")
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

    # Validate file size (limit to 5MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > 5 * 1024 * 1024:
        return "File size exceeds 5MB limit", 400

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
        cur = db.cursor()

        # Insert data into the database
        for _, row in data.iterrows():
            cur.execute(
                "INSERT INTO teams (team_name, wins, losses) VALUES (?, ?, ?) ",
                (row['team_name'], int(row['wins']), int(row['losses']))
            )
        db.commit()

    except Exception as e:
        return f"An error occurred: {str(e)}", 500

    finally:
        os.remove(file_path)

    return "File uploaded and processed successfully", 200


@app.route('/download_standings')
def download_standings():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teams")
    rows = cur.fetchall()

    # Create a CSV file in memory
    import csv
    from io import StringIO
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Team Name', 'Wins', 'Losses'])  # Header row
    writer.writerows(rows)
    output.seek(0)

    # Send the CSV file as a response
    return app.response_class(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=standings.csv"}
    )


@app.route('/clear_standings')
def clear_standings():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM teams")
    conn.commit()
    return "Standings cleared successfully!", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
