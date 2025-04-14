class LeaderboardModel:
    def __init__(self):
        # Initialize an empty leaderboard as a dictionary
        self.scores = {}

    def reset(self):
        """Reset the leaderboard by clearing all scores."""
        self.scores.clear()
