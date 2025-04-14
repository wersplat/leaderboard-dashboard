import pytest
from flask import Flask
from dashboard.routes.api import api_bp  # Assuming this is where the API Blueprint is registered

@pytest.fixture
def app():
    # Create a test Flask app instance
    app = Flask(__name__)
    app.register_blueprint(api_bp)  # Register the API Blueprint with the app
    return app

@pytest.fixture
def client(app):
    # Create a test client for making requests to the Flask app
    return app.test_client()

def test_leaderboard(client):
    # Test the /api/leaderboard route with valid filters
    response = client.get('/api/leaderboard?stat=PTS&limit=5')
    assert response.status_code == 200, "The /api/leaderboard route should return a 200 status code."
    
    data = response.json
    assert "leaderboard" in data, "The response should contain a 'leaderboard' key."
    assert len(data["leaderboard"]) <= 5, "The leaderboard should contain at most 5 entries."
    
    # Add more assertions to validate the leaderboard data