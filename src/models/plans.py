"""
Plan Data Models
"""
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class FoodItem(BaseModel):
    name: str
    quantity: str
    calories: float
    protein: float
    carbs: float
    fat: float
    serving_size: Optional[str] = None

class Meal(BaseModel):
    name: str
    calories: float
    percent: float
    items: List[FoodItem]

class MealPlan(BaseModel):
    breakfast: Meal
    lunch: Meal
    dinner: Meal
    snacks: Meal
    total_calories: float

class Exercise(BaseModel):
    name: str
    sets: int
    reps: str
    rest: str
    notes: Optional[str] = None

class WorkoutDay(BaseModel):
    day: int
    name: str
    exercises: List[Exercise]
    notes: Optional[str] = None

class WorkoutPlan(BaseModel):
    split: str
    days_per_week: int
    workouts: List[WorkoutDay]
    cardio: Optional[Dict[str, str]] = None
    warmup: Optional[str] = None
    cooldown: Optional[str] = None

class NutritionPlan(BaseModel):
    bmr: float
    tdee: float
    calorie_target: float
    macros: Dict[str, Dict[str, float]]
    meal_plan: MealPlan
    recommendations: List[str]

class FullPlan(BaseModel):
    user_id: Optional[str] = None
    generated_date: datetime
    nutrition_plan: NutritionPlan
    workout_plan: WorkoutPlan
    progress_tracking: Optional[Dict] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
