"""
Total Daily Energy Expenditure (TDEE) Calculator
"""
import logging
from typing import Dict, Optional
from .bmr_calculator import BMRCalculator

logger = logging.getLogger(__name__)

class TDEECalculator:
    """
    Calculate Total Daily Energy Expenditure
    """
    
    def __init__(self, bmr_calculator: Optional[BMRCalculator] = None):
        """
        Initialize TDEE Calculator
        
        Args:
            bmr_calculator: BMRCalculator instance
        """
        self.bmr_calculator = bmr_calculator or BMRCalculator()
        self.activity_factors = {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "extra_active": 1.9
        }
        self.goal_adjustments = {
            "fat_loss": -500,
            "maintenance": 0,
            "muscle_gain": 300
        }
    
    def calculate(self, weight_kg: float, height_cm: float, 
                  age: int, gender: str, activity_level: str,
                  goal: str) -> Dict[str, float]:
        """
        Calculate TDEE and goal-adjusted calories
        
        Args:
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
            age: Age in years
            gender: 'male' or 'female'
            activity_level: Activity level key
            goal: Fitness goal
            
        Returns:
            Dictionary with BMR, TDEE, and adjusted calories
        """
        # Calculate BMR
        bmr = self.bmr_calculator.calculate(weight_kg, height_cm, age, gender)
        
        # Calculate TDEE
        activity_factor = self.activity_factors.get(activity_level, 1.55)
        tdee = bmr * activity_factor
        
        # Apply goal adjustment
        adjustment = self.goal_adjustments.get(goal, 0)
        calorie_target = tdee + adjustment
        
        result = {
            "bmr": round(bmr, 1),
            "tdee": round(tdee, 1),
            "calorie_target": round(calorie_target, 1),
            "activity_factor": activity_factor,
            "adjustment": adjustment
        }
        
        logger.info(f"TDEE Calculation: {result}")
        return result
    
    def calculate_weekly(self, weight_kg: float, height_cm: float,
                        age: int, gender: str, activity_level: str,
                        goal: str) -> Dict[str, float]:
        """
        Calculate weekly totals
        """
        daily = self.calculate(weight_kg, height_cm, age, gender, 
                              activity_level, goal)
        
        return {
            **daily,
            "weekly_bmr": round(daily["bmr"] * 7, 1),
            "weekly_tdee": round(daily["tdee"] * 7, 1),
            "weekly_calories": round(daily["calorie_target"] * 7, 1)
        }
