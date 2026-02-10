from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from app.models import RecipeCreate, RecipeUpdate
from app.services.storage import recipe_storage
from app.models import Ingredient, MeasurementUnit

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def parse_ingredients(form):
    ingredients = {}
    
    for key,value in form.items():
        if key.startswith("ingredients["):
            index = int(key.split("[")[1].split("]")[0])
            field = key.split("[")[2].rstrip("]")
            ingredients.setdefault(index, {})[field] = value
        
        return [
            Ingredient(
            quantity=float(data["quantity"]),
            unit=data["unit"],
            item=data["item"]
            )
        for _, data in sorted(ingredients.items())
    ]



@router.get("/", response_class=HTMLResponse)
def home(request: Request, search: Optional[str] = None, message: Optional[str] = None):
    """Home page with recipe list and search"""
    if search:
        recipes = recipe_storage.search_recipes(search)
    else:
        recipes = recipe_storage.get_all_recipes()
    
    return templates.TemplateResponse(request, "index.html", {
        "recipes": recipes,
        "search_query": search or "",
        "message": message,
        "MeasurementUnit": MeasurementUnit

    })


@router.get("/recipes/new", response_class=HTMLResponse)
def new_recipe_form(request: Request):
    """New recipe form"""
    return templates.TemplateResponse(request, "recipe_form.html", {
        "recipe": None,
        "is_edit": False,
        "MeasurementUnit": MeasurementUnit
    })


@router.get("/recipes/{recipe_id}", response_class=HTMLResponse)
def recipe_detail(request: Request, recipe_id: str, message: Optional[str] = None):
    """Recipe detail page"""
    recipe = recipe_storage.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return templates.TemplateResponse(request, "recipe_detail.html", {
        "recipe": recipe,
        "message": message,
        "MeasurementUnit": MeasurementUnit
    })


@router.get("/recipes/{recipe_id}/edit", response_class=HTMLResponse)
def edit_recipe_form(request: Request, recipe_id: str):
    """Edit recipe form"""
    recipe = recipe_storage.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return templates.TemplateResponse(request, "recipe_form.html", {
        "recipe": recipe,
        "is_edit": True,
        "MeasurementUnit": MeasurementUnit
    })


@router.post("/recipes/new")
async def create_recipe_form(request: Request):
    try:
        form = await request.form()

        title = form.get("title", "").strip()
        description = form.get("description", "").strip()
        difficulty = form.get("difficulty", "")
        instructions = form.get("instructions", "").strip()
        tags = form.get("tags", "")

        if len(title) > 200:
            raise ValueError("Title too long")

        ingredients = parse_ingredients(form)
        if not ingredients:
            raise ValueError("At least one ingredient required")

        tag_list = [t.strip() for t in tags.split(",") if t.strip()]

        recipe_data = RecipeCreate(
            title=title,
            description=description,
            difficulty=difficulty,
            ingredients=ingredients,
            instructions=instructions,
            tags=tag_list
        )

        new_recipe = recipe_storage.create_recipe(recipe_data)

        return RedirectResponse(
            url=f"/recipes/{new_recipe.id}?message=Recipe created successfully",
            status_code=303
        )

    except Exception as e:
        return RedirectResponse(
            url=f"/?message=Error creating recipe: {str(e)}",
            status_code=303
        )


@router.post("/recipes/{recipe_id}/edit")
async def update_recipe_form(request: Request, recipe_id: str):
    try:
        form = await request.form()

        title = form.get("title", "").strip()
        description = form.get("description", "").strip()
        difficulty = form.get("difficulty", "")
        instructions = form.get("instructions", "").strip()
        tags = form.get("tags", "")

        if len(title) > 200:
            raise ValueError("Title too long")

        ingredients = parse_ingredients(form)
        if not ingredients:
            raise ValueError("At least one ingredient required")

        tag_list = [t.strip() for t in tags.split(",") if t.strip()]

        recipe_data = RecipeUpdate(
            title=title,
            description=description,
            difficulty=difficulty,
            ingredients=ingredients,
            instructions=instructions,
            tags=tag_list
        )

        updated = recipe_storage.update_recipe(recipe_id, recipe_data)
        if not updated:
            raise ValueError("Recipe not found")

        return RedirectResponse(
            url=f"/recipes/{recipe_id}?message=Recipe updated successfully",
            status_code=303
        )

    except Exception as e:
        return RedirectResponse(
            url=f"/recipes/{recipe_id}?message=Error updating recipe: {str(e)}",
            status_code=303
        )



@router.post("/recipes/{recipe_id}/delete")
def delete_recipe_form(recipe_id: str):
    """Handle recipe deletion"""
    success = recipe_storage.delete_recipe(recipe_id)
    if success:
        return RedirectResponse(
            url="/?message=Recipe deleted successfully",
            status_code=303
        )
    else:
        return RedirectResponse(
            url="/?message=Recipe not found",
            status_code=303
        )


@router.get("/import", response_class=HTMLResponse)
def import_page(request: Request, message: Optional[str] = None):
    """Import recipes page"""
    return templates.TemplateResponse(request, "import.html", {
        "message": message
    })
