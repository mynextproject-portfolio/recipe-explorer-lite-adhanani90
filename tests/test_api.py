"""
Basic smoke and contract tests for Recipe Explorer API.
These tests verify that endpoints exist and return expected status codes.
"""

def test_health_check(client):
    """Smoke test: API is running and responding"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_home_page_loads(client):
    """Smoke test: Home page renders without error"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Recipe Explorer" in response.text


def test_get_all_recipes(client, clean_storage):
    """Contract test: GET /api/recipes returns correct structure"""
    response = client.get("/api/recipes")
    assert response.status_code == 200
    data = response.json()
    assert "recipes" in data
    assert isinstance(data["recipes"], list)


def test_create_and_get_recipe(client, clean_storage, sample_recipe_data):
    """Contract test: Create recipe and verify response structure"""
    # Create recipe
    create_response = client.post("/api/recipes", json=sample_recipe_data)
    assert create_response.status_code == 200
    
    recipe = create_response.json()
    assert "id" in recipe
    assert "title" in recipe
    assert "created_at" in recipe
    assert recipe["title"] == sample_recipe_data["title"]
    
    # Get recipe
    get_response = client.get(f"/api/recipes/{recipe['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == recipe["id"]


def test_recipe_not_found(client, clean_storage):
    """Contract test: Non-existent recipe returns 404"""
    response = client.get("/api/recipes/non-existent-id")
    assert response.status_code == 404


def test_recipe_pages_load(client, clean_storage, sample_recipe_data):
    """Smoke test: Recipe HTML pages load without error"""
    # Create a recipe first
    create_response = client.post("/api/recipes", json=sample_recipe_data)
    recipe_id = create_response.json()["id"]
    
    # Test recipe detail page
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    
    # Test new recipe form
    response = client.get("/recipes/new")
    assert response.status_code == 200
    
    # Test import page
    response = client.get("/import")
    assert response.status_code == 200
