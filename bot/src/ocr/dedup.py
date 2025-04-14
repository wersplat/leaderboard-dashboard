import json
import os
from hashlib import sha256

DEDUP_FILE = "data/dedup_index.json"

def load_index():
    if os.path.exists(DEDUP_FILE):
        with open(DEDUP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_index(index):
    with open(DEDUP_FILE, "w") as f:
        json.dump(index, f, indent=2)

def compute_stat_hash(parsed_result):
    """
    Compute a hash of the important game data for deduplication.
    """
    key = json.dumps(parsed_result, sort_keys=True)
    return sha256(key.encode()).hexdigest()

def is_duplicate(stat_hash):
    index = load_index()
    return stat_hash in index

def record_game(stat_hash, game_id):
    index = load_index()
    index[stat_hash] = game_id
    save_index(index)
