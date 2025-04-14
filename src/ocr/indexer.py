import os
import json
from datetime import datetime

INDEX_FILE = "data/games_index.json"

def load_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
    return []

def save_index(index):
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)

def append_to_index(entry: dict):
    index = load_index()
    index.append(entry)
    save_index(index)

def build_game_index_entry(game_id: str, stat_hash: str, image_url: str = None, source: str = "unknown") -> dict:
    return {
        "game_id": game_id,
        "stat_hash": stat_hash,
        "image_url": image_url,
        "timestamp": datetime.utcnow().isoformat(),
        "source": source
    }

def update_index(game_id: str, stat_hash: str, image_url: str = None, source: str = "unknown"):
    entry = build_game_index_entry(game_id, stat_hash, image_url, source)
    append_to_index(entry)

def search_by_game_id(game_id: str):
    index = load_index()
    return next((entry for entry in index if entry["game_id"] == game_id), None)

def filter_by_source(source: str):
    index = load_index()
    return [entry for entry in index if entry.get("source") == source]

def filter_by_date_range(start: str, end: str):
    """
    Expects ISO 8601 date strings, e.g., "2025-04-01T00:00:00"
    """
    from datetime import datetime
    index = load_index()
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    return [
        entry for entry in index
        if start_dt <= datetime.fromisoformat(entry["timestamp"]) <= end_dt
    ]
