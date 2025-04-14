import discord
from discord.ext import commands
from discord import Option
from sheets.leaderboard import get_leaderboard, get_mvp_totals, get_all_players  # Fetch player names dynamically
from sheets.sheets_api import append_stats_to_sheet, get_game_summary, get_all_game_ids  # Fetch game IDs dynamically
from bot.image_handler import send_image_to_api  # Assuming this function sends image to OCR API
from datetime import datetime
from bot.cooldowns import is_on_cooldown, update_cooldown
import logging

# Configure logging with timestamps
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("discord")

# Slash Command Setup
class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="parse", description="Parse a box score image to extract stats.")
    async def parse(self, ctx):
        user_id = ctx.author.id
        if is_on_cooldown(user_id):
            logger.warning(f"User {user_id} attempted to use 'parse' while on cooldown.")
            await ctx.respond(
                "⏳ You're on cooldown. Please wait before submitting another game.",
                ephemeral=True
            )
            return
        update_cooldown(user_id)

        if not ctx.message.attachments:
            logger.error(f"User {user_id} attempted 'parse' without attaching an image.")
            await ctx.respond(
                "❌ Please attach a box score image with your command.",
                ephemeral=True
            )
            return

        image = ctx.message.attachments[0]
        logger.info(f"User {user_id} uploaded image: {image.filename}")
        await ctx.respond(
            f"📤 Image received: `{image.filename}`\nProcessing..."
        )

        try:
            result = send_image_to_api(image.url)
            if "error" in result:
                logger.error(f"OCR API error for user {user_id}: {result['error']}")
                await ctx.respond(f"❗ Error from OCR API: {result['error']}")
                return

            mvp = result.get("mvp", {}).get("name", "N/A")
            winner = result.get("winner", "N/A")

            embed = discord.Embed(
                title="📊 Game Summary",
                description=f"🏆 **Winner:** {winner}\n⭐ **MVP:** {mvp}",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=image.url)
            await ctx.send(embed=embed)

            sheet_name = datetime.utcnow().strftime("Game-%Y%m%d-%H%M")
            append_stats_to_sheet(result, sheet_name)
            logger.info(f"Game stats saved to Google Sheets tab: {sheet_name}")
            await ctx.send(
                f"📝 Stats saved to tab `{sheet_name}` in Google Sheets."
            )

        except Exception as e:
            logger.exception(f"Unexpected error during 'parse' for user {user_id}: {e}")
            await ctx.send(f"⚠️ An unexpected error occurred while processing the image: {str(e)}")

    @commands.slash_command(name="leaderboard", description="View the top players leaderboard.")
    async def leaderboard(self, ctx, limit: int = 5, team: str = None, season: str = None):
        try:
            # Fetch top players from the leaderboard, apply filters if needed
            top_players = get_leaderboard(limit=limit, team=team, season=season)
            if not top_players:
                await ctx.respond("No leaderboard data available.")
                return

            embed = discord.Embed(
                title="🏀 Top Scorers Leaderboard",
                color=discord.Color.gold()
            )
            for i, (player, pts) in enumerate(top_players, start=1):
                embed.add_field(name=f"#{i} {player}", value=f"{pts} PTS", inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Could not fetch leaderboard: {str(e)}")

    @commands.slash_command(name="resend_game", description="Resend game stats to Google Sheets.")
    async def resend_game(self, ctx, game_id: str):
        try:
            await ctx.respond(f"Resending game {game_id} to Google Sheets...")

        except Exception as e:
            await ctx.send(f"Error resending game data: {str(e)}")

    @commands.slash_command(name="mvp", description="Fetch MVP totals for a player.")
    async def mvp(self, ctx, player: Option(str, "Enter the player's name") -> str):
        try:
            mvp_data = get_mvp_totals(player)
            if not mvp_data:
                await ctx.respond(f"No MVP data found for player `{player}`.")
                return

            embed = discord.Embed(
                title=f"🏆 MVP Totals for {player}",
                description=f"**Total MVP Awards:** {mvp_data['total']}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Could not fetch MVP data: {str(e)}")

    @commands.slash_command(name="game", description="Display a summary of a specific game.")
    async def game(self, ctx, game_id: Option(str, "Enter the game ID") -> str):
        try:
            game_summary = get_game_summary(game_id)
            if not game_summary:
                await ctx.respond(f"No data found for game ID `{game_id}`.")
                return

            embed = discord.Embed(
                title=f"📊 Game Summary: {game_id}",
                description=f"🏆 **Winner:** {game_summary['winner']}\n⭐ **MVP:** {game_summary['mvp']}",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Could not fetch game summary: {str(e)}")

    # Autocomplete for player names
    @mvp.autocomplete("player")
    async def mvp_autocomplete(self, ctx, current: str):
        try:
            # Fetch all player names dynamically
            players = get_all_players()
            # Filter players based on the current input
            return [player for player in players if current.lower() in player.lower()]
        except Exception as e:
            # Log the error and return an empty list if something goes wrong
            print(f"Error fetching player names for autocomplete: {e}")
            return []

    # Autocomplete for game IDs
    @game.autocomplete("game_id")
    async def game_autocomplete(self, ctx, current: str):
        try:
            # Fetch all game IDs dynamically
            game_ids = get_all_game_ids()
            # Filter game IDs based on the current input
            return [game_id for game_id in game_ids if current.lower() in game_id.lower()]
        except Exception as e:
            # Log the error and return an empty list if something goes wrong
            print(f"Error fetching game IDs for autocomplete: {e}")
            return []

# Add the slash commands to the bot
def setup(bot):
    bot.add_cog(SlashCommands(bot))
