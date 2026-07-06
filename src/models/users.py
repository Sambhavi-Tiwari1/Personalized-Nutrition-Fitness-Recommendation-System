"""
User Data Models
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTRA_ACTIVE = "extra_active"

class FitnessGoal(str, Enum):
    FAT_LOSS = "fat_loss"
    MAINTENANCE = "maintenance"
    MUSCLE_GAIN = "muscle_gain"

class DietaryPreference(str, Enum):
    OMNIVORE = "omnivore"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    KETO = "keto"
    MEDITERRANEAN = "mediterranean"
    PALEO = "paleo"
    GLUTEN_FREE = "gluten_free"

class UserProfile(BaseModel):
    """
    User profile for nutrition and fitness planning
    """
    age: int = Field(..., ge=10, le=120, description="Age in years")
    gender: Gender
    weight: float = Field(..., ge=20, le=300, description="Weight in kg")
    height: float = Field(..., ge=100, le=250, description="Height in cm")
    activity_level: ActivityLevel
    goal: FitnessGoal
    dietary_preference: DietaryPreference = DietaryPreference.OMNIVORE
    allergies: List[str] = Field(default_factory=list)
    restrictions: List[str] = Field(default_factory=list)
    experience_level: str = Field(default="intermediate")
    days_per_week: int = Field(default=4, ge=1, le=7)
    medical_conditions: Optional[List[str]] = None
    
    @validator('weight')
    def validate_weight(cls, v):
        if v < 20 or v > 300:
            raise ValueError("Weight must be between 20 and 300 kg")
        return v
    
    @validator('height')
    def validate_height(cls, v):
        if v < 100 or v > 250:
            raise ValueError("Height must be between 100 and 250 cm")
        return v
    
    @validator('age')
    def validate_age(cls, v):
        if v < 10 or v > 120:
            raise ValueError("Age must be between 10 and 120 years")
        return v
    
    class Config:
        use_enum_values = True
