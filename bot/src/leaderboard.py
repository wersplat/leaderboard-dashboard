from .leaderboard.models import LeaderboardModel
from .leaderboard.services import LeaderboardService
from .leaderboard.utils import format_leaderboard

# Initialize the leaderboard model and service
leaderboard_model = LeaderboardModel()
leaderboard_service = LeaderboardService(leaderboard_model)

# Example usage
leaderboard_service.add_user_score("Alice", 100)
leaderboard_service.add_user_score("Bob", 150)
leaderboard_service.add_user_score("Alice", 50)

# Get and format the top users
top_users = leaderboard_service.get_top_users(2)
print(format_leaderboard(top_users))