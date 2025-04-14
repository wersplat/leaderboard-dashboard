from .models import LeaderboardModel

class LeaderboardService:
    def __init__(self, model: LeaderboardModel):
        self.model = model

    def add_user_score(self, user: str, score: int):
        """Add or update a user's score."""
        if user in self.model.scores:
            self.model.scores[user] += score
        else:
            self.model.scores[user] = score

    def get_top_users(self, top_n: int):
        """Retrieve the top N users sorted by score."""
        return sorted(self.model.scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
