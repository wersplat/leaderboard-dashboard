import discord
from discord.ext import commands
import logging
import os
from config.config import BOT_PREFIX

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord")

# Get bot token from environment variable
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Replace hardcoded command prefix with centralized configuration
COMMAND_PREFIX = BOT_PREFIX

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Required to read image attachments

# Initialize bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# On ready
@bot.event
async def on_ready():
    logger.info(f"Bot connected as {bot.user}")

# Load command modules
initial_extensions = [
    "bot.commands",
    "bot.slash"  # New slash command cog
]
for extension in initial_extensions:
    try:
        bot.load_extension(extension)
        logger.info(f"Loaded extension: {extension}")
    except Exception as e:
        logger.error(f"Failed to load extension {extension}: {e}")

# Run bot
if TOKEN:
    bot.run(TOKEN)
else:
    logger.error("DISCORD_BOT_TOKEN not set in environment variables.")