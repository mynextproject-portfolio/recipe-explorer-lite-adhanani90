from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import api, pages
import os

# App configuration
APP_NAME = "Recipe Explorer"
VERSION = "1.0.0"
DEBUG = True

# Create FastAPI app
app = FastAPI(title=APP_NAME, version=VERSION)

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
