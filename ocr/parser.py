import re

def parse_stat_block(text: str) -> dict:
    """
    Parses OCR text into structured team/player stats.
    Returns dict with team1, team2, MVP, and winner.
    """

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    players = []

    # Regex pattern to extract player stat lines
    pattern = re.compile(r"(?P<name>.+?)\s+(?P<pts>\d+)\s*PTS", re.IGNORECASE)

    for line in lines:
        match = pattern.search(line)
        if match:
            players.append({
                "name": match.group("name"),
                "pts": int(match.group("pts"))
            })

    # Dummy logic to split into teams
    midpoint = len(players) // 2
    team1 = players[:midpoint]
    team2 = players[midpoint:]

    # Dummy logic to find MVP and winner
    all_players = team1 + team2
    mvp = max(all_players, key=lambda x: x["pts"], default={"name": "N/A", "pts": 0})
    score1 = sum(p["pts"] for p in team1)
    score2 = sum(p["pts"] for p in team2)
    winner = "Team 1" if score1 >= score2 else "Team 2"

    return {
        "team1": team1,
        "team2": team2,
        "winner": winner,
        "mvp": {
            "name": mvp["name"],
            "line": f"{mvp['pts']} PTS"
        }
    }