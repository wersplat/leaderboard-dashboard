import os
import asyncio
from bot import LeaderboardBot
from database.models import Base, engine

async def main():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

    bot = LeaderboardBot()

    await bot.load_extension('cogs.leaderboard_commands')

    async with bot:
        await bot.start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
