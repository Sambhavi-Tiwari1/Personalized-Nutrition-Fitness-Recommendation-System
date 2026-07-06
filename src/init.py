"""
Personalized Nutrition & Fitness Recommendation System
"""

from .calculators.bmr_calculator import BMRCalculator
from .calculators.tdee_calculator import TDEECalculator
from .calculators.macros_calculator import MacroCalculator
from .recommendation.meal_planner import MealPlanner
from .recommendation.workout_generator import WorkoutGenerator
from .recommendation.adjustments import PlanAdjuster
from .data.food_database import FoodDatabase
from .data.exercise_database import ExerciseDatabase

__version__ = "1.0.0"
__all__ = [
    'BMRCalculator',
    'TDEECalculator',
    'MacroCalculator',
    'MealPlanner',
    'WorkoutGenerator',
    'PlanAdjuster',
    'FoodDatabase',
    'ExerciseDatabase'
]
