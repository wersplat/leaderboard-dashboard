import discord
from discord import app_commands
from discord.ext import commands

class LeaderboardBot(commands.Bot):
    def __init__(self, command_prefix: str = "!", application_id: str = "YOUR_APP_ID"):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            application_id=application_id
        )

    async def setup_hook(self) -> None:
        """Synchronize application commands."""
        try:
            await self.tree.sync()
            print("Application commands synchronized successfully.")
        except Exception as e:
            print(f"Error during setup_hook: {e}")

    async def on_ready(self) -> None:
        """Log a message when the bot is ready."""
        print(f"Bot is ready! Logged in as {self.user}")

    async def on_error(self, event: str, *args, **kwargs) -> None:
        """Handle errors during events."""
        print(f"Error in {event}: {args[0]}")
        # Optionally log the error to a file or monitoring service
