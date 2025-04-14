import os
import sys
import sqlite3
from flask import Flask, g, render_template, request, redirect
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
                cur.execute("DELETE FROM teams")
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
        app.logger.error("No file part in the request.")
        return redirect("https://dashboard.bodegacatsgc.gg")

    file = request.files['file']
    if file.filename == '':
        app.logger.error("No file selected for uploading.")
        return redirect("https://dashboard.bodegacatsgc.gg")

    # Validate file size (limit to 5MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > 5 * 1024 * 1024:
        app.logger.error("File size exceeds the 5MB limit.")
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
            app.logger.error("Unsupported file format.")
            return redirect("https://dashboard.bodegacatsgc.gg")

        # Validate required columns
        required_columns = {'team_name', 'wins', 'losses'}
        if not required_columns.issubset(data.columns):
            app.logger.error("Uploaded file is missing required columns.")
            return redirect("https://dashboard.bodegacatsgc.gg")

        # Remove duplicate teams by keeping the first occurrence
        data = data.drop_duplicates(subset=['team_name'], keep='first')

        # Remove sample teams if real teams are present
        sample_teams = ['Sample Team 1', 'Sample Team 2']
        if not data[data['team_name'].isin(sample_teams)].empty:
            data = data[~data['team_name'].isin(sample_teams)]

        # Insert data into the database
        db = get_db()
        cur = db.cursor()

        for _, row in data.iterrows():
            cur.execute(
                "INSERT INTO teams (team_name, wins, losses) VALUES (?, ?, ?)",
                (row['team_name'], int(row['wins']), int(row['losses']))
            )
        db.commit()
        app.logger.info("Data successfully inserted into the database.")

    except Exception as e:
        app.logger.error(f"Error processing the uploaded file: {e}")
        return redirect("https://dashboard.bodegacatsgc.gg")

    finally:
        os.remove(file_path)

    return redirect("https://dashboard.bodegacatsgc.gg")


@app.route('/download_standings')
def download_standings():
    try:
        db = get_db()
        cur = db.cursor()
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
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM teams")
        db.commit()

        # Insert sample data to reset the standings
        sample_teams = [
            ('Sample Team 1', 0, 0),
            ('Sample Team 2', 0, 0)
        ]
        cur.executemany(
            "INSERT INTO teams (team_name, wins, losses) VALUES (?, ?, ?)",
            sample_teams
        )
        db.commit()

        return "Standings cleared and reset to default successfully!", 200
    except Exception as e:
        app.logger.error(f"Error clearing standings: {e}")
        return "An error occurred while clearing standings.", 500


@app.route('/update_points')
def update_points():
    try:
        db = get_db()
        cur = db.cursor()

        # Define points per win and per game
        points_per_win = 10
        points_per_game = 1
        points_per_loss = 0
        total_points = (points_per_win + points_per_game + points_per_loss)  # 

        # Update points for each team
        cur.execute("SELECT team_name, wins, losses FROM teams")
        teams = cur.fetchall()

        for team in teams:
            team_name, wins, losses = team
            total_games = wins + losses
            points = (wins * points_per_win) + (total_games * points_per_game)

            cur.execute(
                "UPDATE teams SET points = ? WHERE team_name = ?",
                (points, team_name)
            )

        db.commit()
        return "Points updated successfully!", 200
    except Exception as e:
        app.logger.error(f"Error updating points: {e}")
        return "An error occurred while updating points.", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
