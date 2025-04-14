-- Recreate the teams table with constraints included
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    wins INTEGER DEFAULT 0 CHECK (wins >= 0),
    losses INTEGER DEFAULT 0 CHECK (losses >= 0)
);

-- Insert initial data
INSERT INTO teams (team_name, wins, losses) VALUES
('Bodega Cats', 5, 2),
('Midnight Runners', 4, 3),
('Skyline Snipers', 3, 4);

-- Add an index to optimize queries on team_name
CREATE INDEX IF NOT EXISTS idx_team_name ON teams (team_name);
