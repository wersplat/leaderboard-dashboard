import re

def normalize_player_name(name: str) -> str:
    """
    Normalize player name formatting.
    E.g. 'j. SMITH' -> 'J. Smith'
    """
    name = name.strip()
    name = re.sub(r'\s+', ' ', name)
    return name.title()

def normalize_stat_block(data: dict) -> dict:
    """
    Normalize and clean stat block after parsing.
    - Standardize player names
    - Remove empty or malformed entries
    """
    try:
        data["team1"] = clean_team(data.get("team1", []))
        data["team2"] = clean_team(data.get("team2", []))

        # Recalculate MVP
        all_players = data["team1"] + data["team2"]
        if all_players:
            mvp = max(all_players, key=lambda p: p["pts"])
            data["mvp"] = {"name": mvp["name"], "line": f"{mvp['pts']} PTS"}

        return data
    except Exception as e:
        raise ValueError(f"Error normalizing stat block: {e}")

def clean_team(team):
    """Clean and normalize a team by standardizing player names and removing invalid entries."""
    cleaned = []
    for player in team:
        name = normalize_player_name(player.get("name", ""))
        pts = player.get("pts", 0)
        if name and isinstance(pts, int):
            cleaned.append({"name": name, "pts": pts})
    return cleaned

def clean_and_normalize_ocr_data(ocr_data: dict) -> dict:
    """
    Clean and normalize parsed OCR stat data.
    """
    return normalize_stat_block(ocr_data)
