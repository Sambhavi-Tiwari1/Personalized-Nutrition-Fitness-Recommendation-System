"""
FastAPI Application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging
from datetime import datetime

from src.models.user import UserProfile, FitnessGoal, ActivityLevel, DietaryPreference
from src.models.plan import FullPlan
from src.calculators.bmr_calculator import BMRCalculator
from src.calculators.tdee_calculator import TDEECalculator
from src.calculators.macros_calculator import MacroCalculator
from src.recommendation.meal_planner import MealPlanner
from src.recommendation.workout_generator import WorkoutGenerator
from src.recommendation.adjustments import PlanAdjuster
from src.data.food_database import FoodDatabase
from src.data.exercise_database import ExerciseDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Personalized Nutrition & Fitness Recommendation System",
    description="Generate personalized nutrition and fitness plans",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
bmr_calc = BMRCalculator()
tdee_calc = TDEECalculator(bmr_calc)
macro_calc = MacroCalculator()
food_db = FoodDatabase()
exercise_db = ExerciseDatabase()
meal_planner = MealPlanner(food_db)
workout_gen = WorkoutGenerator(exercise_db)
plan_adjuster = PlanAdjuster()

class PlanRequest(BaseModel):
    age: int
    gender: str
    weight: float
    height: float
    activity_level: str
    goal: str
    dietary_preference: str = "omnivore"
    allergies: List[str] = []
    restrictions: List[str] = []
    experience_level: str = "intermediate"
    days_per_week: int = 4

class AdjustRequest(BaseModel):
    current_plan: dict
    weight_change: float
    weeks: int
    goal: str
    performance: Optional[float] = 0.0
    adherence: Optional[float] = 1.0

@app.get("/")
async def root():
    return {
        "message": "Personalized Nutrition & Fitness Recommendation System",
        "version": "1.0.0",
        "endpoints": {
            "/plan/generate": "Generate full plan",
            "/nutrition/calculate": "Calculate nutrition only",
            "/workout/generate": "Generate workout only",
            "/plan/adjust": "Adjust plan based on progress",
            "/foods/search": "Search foods",
            "/exercises/search": "Search exercises"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/plan/generate")
async def generate_plan(request: PlanRequest) -> dict:
    """
    Generate complete personalized plan
    """
    try:
        # Validate input
        user_profile = UserProfile(
            age=request.age,
            gender=request.gender,
            weight=request.weight,
            height=request.height,
            activity_level=request.activity_level,
            goal=request.goal,
            dietary_preference=request.dietary_preference,
            allergies=request.allergies,
            restrictions=request.restrictions
        )
        
        # Calculate BMR and TDEE
        bmr = bmr_calc.calculate(
            user_profile.weight,
            user_profile.height,
            user_profile.age,
            user_profile.gender
        )
        
        tdee_data = tdee_calc.calculate(
            user_profile.weight,
            user_profile.height,
            user_profile.age,
            user_profile.gender,
            user_profile.activity_level,
            user_profile.goal
        )
        
        # Calculate macros
        macros = macro_calc.calculate(
            user_profile.weight,
            tdee_data["calorie_target"],
            user_profile.goal
        )
        
        # Generate meal plan
        meal_plan = meal_planner.generate_plan(
            tdee_data["calorie_target"],
            macros,
            user_profile.dietary_preference,
            user_profile.allergies
        )
        
        # Generate workout plan
        workout_plan = workout_gen.generate_plan(
            user_profile.goal,
            user_profile.experience_level,
            user_profile.days_per_week
        )
        
        # Generate recommendations
        recommendations = generate_recommendations(
            user_profile, tdee_data, macros
        )
        
        # Full plan
        full_plan = {
            "user_profile": user_profile.dict(),
            "metabolic_metrics": {
                "bmr": bmr,
                "tdee": tdee_data["tdee"],
                "calorie_target": tdee_data["calorie_target"],
                "protein": macros["protein"]["grams"],
                "fat": macros["fat"]["grams"],
                "carbs": macros["carbs"]["grams"]
            },
            "meal_plan": meal_plan.dict(),
            "workout_plan": workout_plan.dict(),
            "recommendations": recommendations,
            "generated_date": datetime.now().isoformat()
        }
        
        return full_plan
        
    except Exception as e:
        logger.error(f"Error generating plan: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/nutrition/calculate")
async def calculate_nutrition(request: PlanRequest) -> dict:
    """
    Calculate nutrition plan only
    """
    try:
        user_profile = UserProfile(
            age=request.age,
            gender=request.gender,
            weight=request.weight,
            height=request.height,
            activity_level=request.activity_level,
            goal=request.goal
        )
        
        bmr = bmr_calc.calculate(
            user_profile.weight,
            user_profile.height,
            user_profile.age,
            user_profile.gender
        )
        
        tdee_data = tdee_calc.calculate(
            user_profile.weight,
            user_profile.height,
            user_profile.age,
            user_profile.gender,
            user_profile.activity_level,
            user_profile.goal
        )
        
        macros = macro_calc.calculate(
            user_profile.weight,
            tdee_data["calorie_target"],
            user_profile.goal
        )
        
        meal_plan = meal_planner.generate_plan(
            tdee_data["calorie_target"],
            macros,
            request.dietary_preference,
            request.allergies
        )
        
        return {
            "bmr": bmr,
            "tdee": tdee_data["tdee"],
            "calorie_target": tdee_data["calorie_target"],
            "macros": macros,
            "meal_plan": meal_plan.dict()
        }
        
    except Exception as e:
        logger.error(f"Error calculating nutrition: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/workout/generate")
async def generate_workout(request: dict) -> dict:
    """
    Generate workout plan only
    """
    try:
        goal = request.get("goal", "maintenance")
        experience_level = request.get("experience_level", "intermediate")
        days_per_week = request.get("days_per_week", 4)
        
        workout_plan = workout_gen.generate_plan(
            goal,
            experience_level,
            days_per_week
        )
        
        return workout_plan.dict()
        
    except Exception as e:
        logger.error(f"Error generating workout: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/plan/adjust")
async def adjust_plan(request: AdjustRequest) -> dict:
    """
    Adjust plan based on progress
    """
    try:
        adjustments = plan_adjuster.get_plan_adjustments(
            request.current_plan,
            {
                "weight_change": request.weight_change,
                "weeks": request.weeks,
                "goal": request.goal,
                "performance": request.performance,
                "adherence": request.adherence
            },
            request.weeks
        )
        
        return adjustments
        
    except Exception as e:
        logger.error(f"Error adjusting plan: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/foods/search")
async def search_foods(query: str, limit: int = 10) -> dict:
    """
    Search for foods
    """
    try:
        results = food_db.search_foods(query, limit)
        return {"results": results}
        
    except Exception as e:
        logger.error(f"Error searching foods: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/exercises/search")
async def search_exercises(muscle: str = None, level: str = "intermediate") -> dict:
    """
    Search for exercises
    """
    try:
        if muscle:
            results = exercise_db.get_exercises_by_muscle(muscle, level)
        else:
            results = exercise_db.exercises.to_dict('records')
        
        return {"results": results}
        
    except Exception as e:
        logger.error(f"Error searching exercises: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def generate_recommendations(user_profile, tdee_data, macros):
    """Generate personalized recommendations"""
    recommendations = []
    
    # Protein recommendation
    if user_profile.goal == "muscle_gain":
        recommendations.append(f"Increase protein intake to {macros['protein']['grams']:.1f}g daily for optimal muscle synthesis")
    elif user_profile.goal == "fat_loss":
        recommendations.append(f"Maintain high protein intake ({macros['protein']['grams']:.1f}g) to preserve muscle during fat loss")
    
    # Meal timing
    recommendations.append("Distribute meals evenly throughout the day")
    recommendations.append("Consume carbohydrates around workout times for optimal energy")
    
    # Hydration
    recommendations.append("Stay hydrated - aim for 2.5-3L of water daily")
    
    # Sleep
    recommendations.append("Get 7-9 hours of quality sleep for optimal recovery")
    
    # Meal prep
    recommendations.append("Prepare meals in advance to stay consistent with your plan")
    
    # Progress tracking
    recommendations.append("Track your progress weekly and adjust as needed")
    
    return recommendations
