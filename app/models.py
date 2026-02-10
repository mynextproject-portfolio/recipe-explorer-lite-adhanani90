from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum
import uuid

# Constants
MAX_TITLE_LENGTH = 200
MAX_INGREDIENTS = 50

class DifficultyLevel(str, Enum):
    def __str__(self):
        return self.value
    EASY = "Easy"
    MEDIUM = "Medium" 
    HARD = "Hard"
    
class MeasurementUnit(str, Enum):
    def __str__(self):
        return self.value
    # Volume
    ML = "ml"
    L = "liter"
    TSP = "teaspoon"
    TBSP = "tablespoon"
    FL_OZ = "fl oz"
    CUP = "cup"
    PINT = "pint"
    QUART = "quart"
    
    # Weight
    G = "grams"
    KG = "kg"
    OZ = "oz"
    LB = "lb"
    
    # Other
    PINCH = "pinch"
    WHOLE = "whole"
    PIECE = "piece"
    
class Ingredient(BaseModel):
    quantity: float
    unit: MeasurementUnit
    item: str

class Recipe(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str 
    description: str
    ingredients: List[Ingredient]
    instructions: List[str]
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    cuisine: str


    


class RecipeCreate(BaseModel):
    title: str
    description: str
    ingredients: List[Ingredient]
    instructions: List[str]
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel
    cuisine:str


class RecipeUpdate(BaseModel):
    title: str
    description: str
    ingredients: List[Ingredient]
    instructions: List[str]
    tags: List[str]
    difficulty: DifficultyLevel
    cuisine:str