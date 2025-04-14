-- Recreate the teams table with constraints included
CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    team_name TEXT NOT NULL UNIQUE,
    wins INTEGER DEFAULT 0 CHECK (wins >= 0),
    losses INTEGER DEFAULT 0 CHECK (losses >= 0),
    total_points INTEGER DEFAULT 0 CHECK (total_points >= 0),
    games_played INTEGER GENERATED ALWAYS AS (wins + losses) STORED,
    win_rate REAL GENERATED ALWAYS AS (CAST(wins AS FLOAT) / NULLIF(games_played, 0)) STORED,
    division TEXT
);

-- Insert initial data
INSERT INTO teams (team_name, wins, losses, total_points) VALUES
('Team A', 5, 2, 52),
('Team B', 4, 3, 47),
('Team C', 3, 4, 37);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_team_name ON teams (team_name);
CREATE INDEX IF NOT EXISTS idx_wins ON teams (wins);
CREATE INDEX IF NOT EXISTS idx_wins_losses ON teams (wins, losses);
