from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import api, pages
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import json
from app.services.storage import recipe_storage


 


# App configuration
APP_NAME = "Recipe Explorer"
VERSION = "1.0.0"
DEBUG = True

@asynccontextmanager 
async def lifespan(app:FastAPI):
    #app startup
    recipe_file = "sample-recipes.json"
    if os.path.exists(recipe_file):
        try:
            with open(recipe_file, "r") as f:
                singleRecipe = json.load(f)[0]
            recipe_storage.import_recipes([singleRecipe])
        except Exception as e:
            print(f"✗ Error loading recipes: {e}")
    yield
    
 

# Create FastAPI app
app = FastAPI(title=APP_NAME, version=VERSION, lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


            


# Include routers
app.include_router(api.router)
app.include_router(pages.router)

# Basic health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# @app.get("/status")
# def status():
#     return {"status": "ok", "version": "1.0.0"}
