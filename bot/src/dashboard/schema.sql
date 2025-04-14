
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
