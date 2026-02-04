from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum
import uuid

# Constants
MAX_TITLE_LENGTH = 200
MAX_INGREDIENTS = 50

class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium" 
    HARD = "Hard"

class Recipe(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str 
    description: str
    ingredients: List[str]
    instructions: str
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class RecipeCreate(BaseModel):
    title: str
    description: str
    ingredients: List[str]
    instructions: str
    tags: List[str] = Field(default_factory=list)
    difficulty: DifficultyLevel


class RecipeUpdate(BaseModel):
    title: str
    description: str
    ingredients: List[str]
    instructions: str
    tags: List[str]
    difficulty: DifficultyLevel
