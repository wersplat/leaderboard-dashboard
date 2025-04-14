-- Recreate the teams table with constraints included
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    wins INTEGER DEFAULT 0 CHECK (wins >= 0),
    losses INTEGER DEFAULT 0 CHECK (losses >= 0)
);

-- Insert initial data
INSERT INTO teams (team_name, wins, losses,total_points) VALUES
('Team A', 5, 2, 52),
('Team B', 4, 3, 47),
('Team C', 3, 4, 37);

-- Add an index to optimize queries on team_name
CREATE INDEX IF NOT EXISTS idx_team_name ON teams (team_name);

CREATE INDEX IF NOT EXISTS idx_wins ON teams (wins);

-- Add a new column for total points earned
ALTER TABLE teams ADD COLUMN points INTEGER DEFAULT 0 CHECK (points >= 0);
