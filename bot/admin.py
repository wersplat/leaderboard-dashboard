import discord
from datetime import datetime
from sheets.sheets_api import append_stats_to_sheet
import logging
import os
from config.config import SHEET_NAME

# Admin-only commands; set ADMIN_IDS in .env (comma-separated Discord user IDs)
logger = logging.getLogger("discord")

# Dummy game cache (replace with real lookup later)
game_cache = {}

def is_admin(user_id: int) -> bool:
    """
    Checks if a user is an admin based on their Discord ID.

    Args:
        user_id (int): The Discord user ID.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    admin_ids = os.getenv("ADMIN_USER_IDS", "").split(",")
    return str(user_id) in admin_ids

class AdminControls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="resend_game")
    async def resend_game(self, ctx, game_id: str):
        """
        Re-push a game's data to Google Sheets.
        """
        if not is_admin(ctx.author.id):
            logger.warning(f"Unauthorized attempt by {ctx.author} ({ctx.author.id}) to use {ctx.command}.")
            await ctx.send("🚫 You do not have permission to use this command.")
            return

        if game_id not in game_cache:
            await ctx.send(f"❌ Game `{game_id}` not found in the cache.")
            return

        try:
            data = game_cache[game_id]
            append_stats_to_sheet(data, game_id)
            await ctx.send(f"✅ Game `{game_id}` re-sent to Google Sheets.")
        except Exception as e:
            logger.error(f"Failed to resend game: {e}")
            await ctx.send(f"⚠️ Failed to resend game to Google Sheets. Error: {e}")

    @commands.command(name="delete_game")
    async def delete_game(self, ctx, game_id: str):
        """
        Deletes a tab in the Google Sheet by game ID.
        """
        if not is_admin(ctx.author.id):
            logger.warning(f"Unauthorized attempt by {ctx.author} ({ctx.author.id}) to use {ctx.command}.")
            await ctx.send("🚫 You do not have permission to use this command.")
            return

        try:
            # Deleting the game from the sheet
            client = append_stats_to_sheet.__globals__['get_sheets_client']()
            sheet = client.open_by_key(append_stats_to_sheet.__globals__['SHEET_ID'])
            worksheet = sheet.worksheet(game_id)

            if worksheet:
                sheet.del_worksheet(worksheet)
                await ctx.send(f"🗑️ Game `{game_id}` tab deleted from Google Sheets.")
            else:
                await ctx.send(f"❌ No tab found for game `{game_id}`.")
        except Exception as e:
            logger.error(f"Failed to delete game tab: {e}")
            await ctx.send(f"⚠️ Could not delete the game tab. Please try again. Error: {e}")

# Example usage of centralized configuration
logger.info(f"Default sheet name is set to: {SHEET_NAME}")

def setup(bot):
    bot.add_cog(AdminControls(bot))
