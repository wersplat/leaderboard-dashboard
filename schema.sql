CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0
);

INSERT INTO teams (team_name, wins, losses) VALUES
('Bodega Cats', 5, 2),
('Midnight Runners', 4, 3),
('Skyline Snipers', 3, 4);

-- Add an index to optimize queries on team_name
CREATE INDEX IF NOT EXISTS idx_team_name ON teams (team_name);

-- Ensure wins and losses are non-negative
ALTER TABLE teams ADD CONSTRAINT chk_wins_nonnegative CHECK (wins >= 0);
ALTER TABLE teams ADD CONSTRAINT chk_losses_nonnegative CHECK (losses >= 0);
