import discord
from discord import app_commands
from discord.ext import commands

class LeaderboardBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id="YOUR_APP_ID"
        )
        
    async def setup_hook(self):
        await self.tree.sync()
        
    async def on_ready(self):
        print(f"Bot is ready! Logged in as {self.user}")
        
    async def on_error(self, event, *args, **kwargs):
        print(f"Error in {event}: {args[0]}")

bot = LeaderboardBot()
