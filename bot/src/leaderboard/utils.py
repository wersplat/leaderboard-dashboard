# Utility functions for leaderboard-related tasks can be added here

# Example utility function
def format_leaderboard(leaderboard):
    """Format the leaderboard for display."""
    return "\n".join([f"{user}: {score}" for user, score in leaderboard])
