class Leaderboard:
    def __init__(self, name: str):
        self.name = name
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def get_top_entries(self, limit: int = 10):
        return sorted(self.entries, key=lambda x: x.score, reverse=True)[:limit]

    def __repr__(self):
        return f"Leaderboard(name={self.name}, entries={len(self.entries)})"
