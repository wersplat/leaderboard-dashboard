import discord
from discord import app_commands
from discord.ext import commands
from ...database.models import LeaderboardEntry

class LeaderboardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="leaderboard", description="View the current leaderboard")
    async def view_leaderboard(self, interaction: discord.Interaction):
        # Fetch top 10 entries from database
        entries = LeaderboardEntry.get_top(10)
        
        embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.gold())
        for i, entry in enumerate(entries, 1):
            embed.add_field(
                name=f"#{i} {entry.user.name}",
                value=f"Score: {entry.score}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="add_score", description="Add or update a user's score")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add_score(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        score: int
    ):
        # Add or update score in database
        LeaderboardEntry.update_score(user.id, score)
        await interaction.response.send_message(
            f"Updated score for {user.mention} to {score}"
        )

    @app_commands.command(name="reset", description="Reset the leaderboard")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset_leaderboard(self, interaction: discord.Interaction):
        # Reset leaderboard in database
        LeaderboardEntry.reset_all()
        await interaction.response.send_message(
            "Leaderboard has been reset!",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(LeaderboardCommands(bot))
