from .leaderboard import Leaderboard

# Initialize the leaderboard
leaderboard = Leaderboard()

# Example command to add a user's score
def add_score_command(user: str, score: int):
    leaderboard.add_user_score(user, score)
    return f"Added {score} points to {user}."

# Example command to view the leaderboard
def view_leaderboard_command(top_n: int):
    top_users = leaderboard.get_top_users(top_n)
    return "\n".join([f"{user}: {score}" for user, score in top_users])

# Example command to reset the leaderboard
def reset_leaderboard_command():
    leaderboard.reset_leaderboard()
    return "Leaderboard has been reset."