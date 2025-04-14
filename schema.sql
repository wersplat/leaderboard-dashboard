-- Recreate the teams table with constraints included
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    wins INTEGER DEFAULT 0 CHECK (wins >= 0),
    losses INTEGER DEFAULT 0 CHECK (losses >= 0),
    total_points INTEGER DEFAULT 0 CHECK (total_points >= 0)
);

-- Insert initial data
INSERT INTO teams (team_name, wins, losses,total_points) VALUES
('Team A', 5, 2, 52),
('Team B', 4, 3, 47),
('Team C', 3, 4, 37);

-- Add an index to optimize queries on team_name
CREATE INDEX IF NOT EXISTS idx_team_name ON teams (team_name);

CREATE INDEX IF NOT EXISTS idx_wins ON teams (wins);

-- Add a last_updated column to track record modifications
ALTER TABLE teams ADD COLUMN last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Add a games_played column to store total games played
ALTER TABLE teams ADD COLUMN games_played INTEGER GENERATED ALWAYS AS (wins + losses) STORED;

-- Add a unique constraint on team_name to prevent duplicates
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_team_name ON teams (team_name);

-- Add a composite index on wins and losses for optimized queries
CREATE INDEX IF NOT EXISTS idx_wins_losses ON teams (wins, losses);

-- Add a win_rate column to calculate win percentage dynamically
ALTER TABLE teams ADD COLUMN win_rate REAL GENERATED ALWAYS AS (CAST(wins AS REAL) / NULLIF(games_played, 0)) STORED;

-- Add a division column to categorize teams into groups
ALTER TABLE teams ADD COLUMN division TEXT;

-- Create an audit_log table to track changes to the teams table
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER,
    action TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams (id)
);

-- Add a check constraint to ensure total_points is consistent with wins
ALTER TABLE teams ADD CONSTRAINT chk_total_points CHECK (total_points >= (wins * 10));

-- Create triggers to log changes in the teams table
CREATE TRIGGER IF NOT EXISTS trg_insert_teams AFTER INSERT ON teams
BEGIN
    INSERT INTO audit_log (team_id, action) VALUES (NEW.id, 'INSERT');
END;

CREATE TRIGGER IF NOT EXISTS trg_update_teams AFTER UPDATE ON teams
BEGIN
    INSERT INTO audit_log (team_id, action) VALUES (NEW.id, 'UPDATE');
END;

CREATE TRIGGER IF NOT EXISTS trg_delete_teams AFTER DELETE ON teams
BEGIN
    INSERT INTO audit_log (team_id, action) VALUES (OLD.id, 'DELETE');
END;
