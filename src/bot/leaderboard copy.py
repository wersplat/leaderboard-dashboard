class Leaderboard:
    def __init__(self):
        # Initialize an empty dictionary to store user stats
        self.stats = {}

    def add_user_result(self, user, result, points):
        """Add or update a user's stats based on the result and points."""
        if user not in self.stats:
            self.stats[user] = {"wins": 0, "losses": 0, "points": 0}

        if result == "win":
            self.stats[user]["wins"] += 1
        elif result == "loss":
            self.stats[user]["losses"] += 1

        self.stats[user]["points"] += points

    def get_top_users(self, top_n=10):
        """Retrieve the top N users sorted by points."""
        return sorted(self.stats.items(), key=lambda x: x[1]["points"], reverse=True)[:top_n]

    def reset_leaderboard(self):
        """Reset the leaderboard by clearing all stats."""
        self.stats.clear()
