"""
Basal Metabolic Rate (BMR) Calculator
"""
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class BMRCalculator:
    """
    Calculate Basal Metabolic Rate using various equations
    """
    
    def __init__(self, equation: str = "mifflin_st_jeor"):
        """
        Initialize BMR Calculator
        
        Args:
            equation: 'mifflin_st_jeor' or 'harris_benedict'
        """
        self.equation = equation
        
    def calculate(self, weight_kg: float, height_cm: float, 
                  age: int, gender: str) -> float:
        """
        Calculate BMR
        
        Args:
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
            age: Age in years
            gender: 'male' or 'female'
            
        Returns:
            BMR in calories per day
        """
        if self.equation == "mifflin_st_jeor":
            return self._mifflin_st_jeor(weight_kg, height_cm, age, gender)
        else:
            return self._harris_benedict(weight_kg, height_cm, age, gender)
    
    def _mifflin_st_jeor(self, weight_kg: float, height_cm: float, 
                         age: int, gender: str) -> float:
        """
        Mifflin-St Jeor Equation
        Most accurate for general population
        """
        if gender.lower() == "male":
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
        
        logger.info(f"BMR calculated (Mifflin-St Jeor): {bmr:.0f} kcal/day")
        return bmr
    
    def _harris_benedict(self, weight_kg: float, height_cm: float, 
                         age: int, gender: str) -> float:
        """
        Harris-Benedict Equation (Revised)
        """
        if gender.lower() == "male":
            bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
        
        logger.info(f"BMR calculated (Harris-Benedict): {bmr:.0f} kcal/day")
        return bmr
    
    def get_activity_factors(self) -> Dict[str, float]:
        """
        Get activity level multipliers for TDEE calculation
        """
        return {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "extra_active": 1.9
        }
    
    def get_goal_adjustments(self) -> Dict[str, int]:
        """
        Get calorie adjustments for different goals
        """
        return {
            "fat_loss": -500,
            "maintenance": 0,
            "muscle_gain": 300
        }
