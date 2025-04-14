import pytest
from discord.ext import commands
from discord import Interaction
from bot.slash import SlashCommands  # Assuming SlashCommands is defined here

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    bot.add_cog(SlashCommands(bot))
    return bot

@pytest.fixture
def mock_interaction():
    # Mocking an interaction context for slash commands
    return Interaction(data={'name': 'parse', 'type': 1}, client=None, state=None, user=None, guild=None)

def test_parse(bot, mock_interaction):
    # Test that the /parse command works correctly
    command = bot.get_command("parse")
    
    # Simulate the slash command execution
    assert command is not None, "The /parse command should be registered."
    
    # Mock the interaction context and simulate execution
    response = command.callback(mock_interaction)
    assert response is not None, "The /parse command should return a response."
    
    # Add more assertions as needed to validate the behavior

def test_leaderboard(bot, mock_interaction):
    # Test that the /leaderboard command shows the leaderboard
    command = bot.get_command("leaderboard")
    
    # Simulate the slash command execution
    response = command.callback(mock_interaction)
    
    # Assert that the response is the expected one
    assert response is not None
    assert "Top Players Leaderboard" in response.content  # Example assertion