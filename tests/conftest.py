"""
Test fixtures for Recipe Explorer tests.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.storage import recipe_storage


@pytest.fixture
def client():
    """Test client for making requests to the API"""
    return TestClient(app)


@pytest.fixture
def clean_storage():
    """Reset storage before and after each test"""
    recipe_storage.recipes.clear()
    yield
    recipe_storage.recipes.clear()


@pytest.fixture
def sample_recipe_data():
    """Sample recipe for testing"""
    return {
        "title": "Test Recipe",
        "description": "A test recipe",
        "ingredients": ["ingredient 1", "ingredient 2"],
        "instructions": "First, do step 1.\n\nThen, do step 2.",
        "tags": ["test"],
        "difficulty": "Easy"
    }
