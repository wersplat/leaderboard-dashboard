from discord.ext import commands
import discord
from src.bot.image_handler import send_image_to_api
from datetime import datetime
from sheets.sheets_api import append_stats_to_sheet, get_game_data_by_id  # Assuming these functions exist
from sheets.leaderboard import get_leaderboard
from bot.cooldowns import is_on_cooldown, update_cooldown
from ...utils.logging import setup_logging

logger = setup_logging()

class ParseCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="parse", description="Parse a box score image to extract stats.")
    async def parse(self, ctx):
        user_id = ctx.author.id
        if is_on_cooldown(user_id):
            logger.warning(f"User {user_id} attempted to use 'parse' while on cooldown.")
            await ctx.send(
                "⏳ You're on cooldown. Please wait before submitting another game."
            )
            return
        update_cooldown(user_id)

        if not ctx.message.attachments:
            logger.error(f"User {user_id} attempted 'parse' without attaching an image.")
            await ctx.send(
                "❌ Please attach a box score image with your command.", ephemeral=True
            )
            return

        image = ctx.message.attachments[0]
        logger.info(f"User {user_id} uploaded image: {image.filename}")
        await ctx.send(
            f"📤 Image received: `{image.filename}`\nProcessing..."
        )

        try:
            result = send_image_to_api(image.url)
            if "error" in result:
                logger.error(f"OCR API error for user {user_id}: {result['error']}")
                await ctx.send(f"❗ Error from OCR API: {result['error']}")
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

    @commands.hybrid_command(name="leaderboard", description="View the top players leaderboard.")
    async def leaderboard(self, ctx, limit: int = 5, team: str = None, season: str = None):
        try:
            top_players = get_leaderboard(limit=limit, team=team, season=season)
            if not top_players:
                await ctx.send("No leaderboard data available.")
                return

            embed = discord.Embed(
                title="🏀 Top Scorers Leaderboard",
                color=discord.Color.gold()
            )
            for i, (player, pts) in enumerate(top_players, start=1):
                embed.add_field(name=f"#{i} {player}", value=f"{pts} PTS", inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error fetching leaderboard: {e}")
            await ctx.send(f"⚠️ Could not fetch leaderboard: {str(e)}")

    @commands.hybrid_command(name="resend_game", description="Resend game stats to Google Sheets.")
    async def resend_game(self, ctx, game_id: str):
        try:
            game_data = get_game_data_by_id(game_id)  # Assuming this function exists

            if not game_data:
                await ctx.send(f"❌ No data found for game ID `{game_id}`.")
                return

            sheet_name = datetime.utcnow().strftime("Game-%Y%m%d-%H%M")
            append_stats_to_sheet(game_data, sheet_name)
            await ctx.send(f"✅ Game {game_id} data has been successfully resent to Google Sheets under tab `{sheet_name}`.")

        except Exception as e:
            logger.error(f"Error resending game {game_id}: {e}")
            await ctx.send(f"⚠️ Error resending game data: {str(e)}")

def setup(bot):
    bot.add_cog(ParseCommands(bot))