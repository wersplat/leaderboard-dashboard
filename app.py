import os
import sys
import sqlite3
from flask import Flask, g, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import pandas as pd
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
                # Insert sample data only if the table is empty
                cur.execute(
                    "INSERT INTO teams (team_name, wins, losses) VALUES "
                    "('Team A', 10, 5)"
                )
                cur.execute(
                    "INSERT INTO teams (team_name, wins, losses) VALUES "
                    "('Team B', 7, 8)"
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


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file part", "error")
        return redirect("https://dashboard.bodegacatsgc.gg")

    file = request.files['file']
    if file.filename == '':
        flash("No selected file", "error")
        return redirect("https://dashboard.bodegacatsgc.gg")

    # Validate file size (limit to 5MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > 5 * 1024 * 1024:
        flash("File size exceeds 5MB limit", "error")
        return redirect("https://dashboard.bodegacatsgc.gg")

    filename = secure_filename(file.filename)
    file_path = os.path.join('/tmp', filename)
    file.save(file_path)

    try:
        if filename.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif filename.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        else:
            flash("Unsupported file format", "error")
            return redirect("https://dashboard.bodegacatsgc.gg")

        # Validate required columns
        required_columns = {'team_name', 'wins', 'losses'}
        if not required_columns.issubset(data.columns):
            missing_columns = required_columns - set(data.columns)
            flash(f"Missing required columns: {missing_columns}", "error")
            return redirect("https://dashboard.bodegacatsgc.gg")

        db = get_db()
        cur = db.cursor()

        # Insert data into the database
        for _, row in data.iterrows():
            cur.execute(
                "INSERT INTO teams (team_name, wins, losses) VALUES (?, ?, ?)",
                (row['team_name'], int(row['wins']), int(row['losses']))
            )
        db.commit()

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect("https://dashboard.bodegacatsgc.gg")

    finally:
        os.remove(file_path)

    flash("File uploaded and processed successfully", "success")
    return redirect("https://dashboard.bodegacatsgc.gg")


@app.route('/download_standings')
def download_standings():
    try:
        conn = get_db_connection()
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
    except Exception as e:
        app.logger.error(f"Error generating standings: {e}")
        return "An error occurred while generating standings.", 500


@app.route('/clear_standings')
def clear_standings():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM teams")
        conn.commit()
        return "Standings cleared successfully!", 200
    except Exception as e:
        app.logger.error(f"Error clearing standings: {e}")
        return "An error occurred while clearing standings.", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
