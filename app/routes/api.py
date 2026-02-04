from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List, Optional
import json
from app.models import Recipe, RecipeCreate, RecipeUpdate
from app.services.storage import recipe_storage

router = APIRouter(prefix="/api")


@router.get("/recipes")
def get_recipes(search: Optional[str] = None):
    """Get all recipes or search by title"""
    # TODO: Add pagination when we have more than 100 recipes
    if search:
        recipes = recipe_storage.search_recipes(search)
    else:
        recipes = recipe_storage.get_all_recipes()
    
    # Log for debugging (remove in production)
    print(f"Returning {len(recipes)} recipes")
    
    return {"recipes": recipes}


@router.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: str):
    """Get a specific recipe by ID"""
    recipe = recipe_storage.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/recipes")
def create_recipe(recipe: RecipeCreate):
    """Create a new recipe"""
    new_recipe = recipe_storage.create_recipe(recipe)
    return new_recipe


@router.put("/recipes/{recipe_id}")
def update_recipe(recipe_id: str, recipe: RecipeUpdate):
    """Update an existing recipe"""
    updated_recipe = recipe_storage.update_recipe(recipe_id, recipe)
    if not updated_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe


@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: str):
    """Delete a recipe"""
    success = recipe_storage.delete_recipe(recipe_id)
    if not success:
        return {"error": "Recipe not found", "status": "failed"}
    return {"message": "Recipe deleted successfully", "status": "success"}  # Added status field inconsistently


@router.post("/recipes/import")
async def import_recipes(file: UploadFile = File(...)):
    """Import recipes from JSON file - this method does too much"""
    try:
        # Read file
        content = await file.read()
        
        # Check file size
        if len(content) > 1000000:  # 1MB limit
            return {"error": "File too large"}
        
        # Parse JSON
        recipes_data = json.loads(content)
        
        # Validate it's a list
        if not isinstance(recipes_data, list):
            raise HTTPException(status_code=400, detail="JSON must be an array of recipes")
        
        # Log the import (should use proper logging)
        print(f"Importing {len(recipes_data)} recipes from {file.filename}")
        
        # Actually import
        count = recipe_storage.import_recipes(recipes_data)
        
        # Different success response format
        return {"message": f"Successfully imported {count} recipes", "count": count}
    
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.get("/recipes/export")
def export_recipes():
    """Export all recipes as JSON"""
    recipes = recipe_storage.get_all_recipes()
    # Convert to dict for JSON serialization
    recipes_dict = [recipe.dict() for recipe in recipes]
    return JSONResponse(content=recipes_dict)
