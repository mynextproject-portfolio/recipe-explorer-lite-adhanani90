# Recipe Explorer

A simple FastAPI web application for managing recipes. Features CRUD operations, search, file uploads, and a Bootstrap frontend.

**Tech Stack:** FastAPI, Jinja2, Bootstrap 5, pytest

## Quick Start

### Run Locally

```bash
# Clone and setup
git clone <repository-url>
cd recipe-explorer-template
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install and run
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit **http://localhost:8000**

### Run with Docker

```bash
docker build -t recipe-explorer .
docker run -p 8000:8000 recipe-explorer
```

Visit **http://localhost:8000**

## Sample Data

Upload the `sample-recipes.json` file using the "Import Recipes" page to get started with 3 example recipes (Poutine, Shuba, Guo Bao Rou).

## Testing

```bash
pytest           # Run all tests
pytest -v        # Verbose output
```

## API Endpoints

**Pages:**
- `/` - Home page with recipe list
- `/recipes/new` - Add recipe form  
- `/recipes/{id}` - Recipe detail page
- `/import` - Import recipes

**API:**
- `GET /api/recipes` - List/search recipes
- `POST /api/recipes` - Create recipe
- `GET /api/recipes/{id}` - Get recipe
- `PUT /api/recipes/{id}` - Update recipe
- `DELETE /api/recipes/{id}` - Delete recipe
- `POST /api/recipes/import` - Import JSON
- `GET /api/recipes/export` - Export JSON

---

*Part of [mynextproject.dev](https://mynextproject.dev) - Learn to code like a professional*
