"""
Macronutrient Distribution Calculator
"""
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class MacroCalculator:
    """
    Calculate macronutrient distribution based on goals
    """
    
    def __init__(self):
        self.protein_range = (1.6, 2.2)  # g per kg body weight
        self.fat_range = (0.20, 0.35)    # Percentage of calories
        self.calories_per_gram = {
            "protein": 4,
            "carbs": 4,
            "fat": 9
        }
    
    def calculate(self, weight_kg: float, total_calories: float,
                  goal: str, protein_factor: Optional[float] = None) -> Dict[str, Dict]:
        """
        Calculate macronutrient distribution
        
        Args:
            weight_kg: Body weight in kilograms
            total_calories: Total daily calorie target
            goal: Fitness goal
            protein_factor: Custom protein factor (g/kg)
            
        Returns:
            Dictionary with macronutrient breakdown
        """
        # Determine protein factor
        if protein_factor:
            protein_factor = protein_factor
        elif goal == "muscle_gain":
            protein_factor = 2.0
        elif goal == "maintenance":
            protein_factor = 1.8
        else:  # fat_loss
            protein_factor = 2.2
        
        # Calculate protein
        protein_grams = weight_kg * protein_factor
        protein_calories = protein_grams * self.calories_per_gram["protein"]
        
        # Calculate fat (30% of calories)
        fat_percent = 0.30
        fat_calories = total_calories * fat_percent
        fat_grams = fat_calories / self.calories_per_gram["fat"]
        
        # Calculate carbs (remaining calories)
        remaining_calories = total_calories - protein_calories - fat_calories
        carbs_grams = remaining_calories / self.calories_per_gram["carbs"]
        
        # Calculate percentages
        protein_percent = (protein_calories / total_calories) * 100
        fat_percent_actual = (fat_calories / total_calories) * 100
        carbs_percent = (remaining_calories / total_calories) * 100
        
        result = {
            "protein": {
                "grams": round(protein_grams, 1),
                "calories": round(protein_calories, 1),
                "percent": round(protein_percent, 1)
            },
            "fat": {
                "grams": round(fat_grams, 1),
                "calories": round(fat_calories, 1),
                "percent": round(fat_percent_actual, 1)
            },
            "carbs": {
                "grams": round(carbs_grams, 1),
                "calories": round(remaining_calories, 1),
                "percent": round(carbs_percent, 1)
            }
        }
        
        logger.info(f"Macronutrient distribution: {result}")
        return result
    
    def get_meal_distribution(self, total_calories: float) -> Dict[str, float]:
        """
        Distribute calories across meals
        
        Returns:
            Meal distribution with calorie counts
        """
        distribution = {
            "breakfast": 0.25,
            "lunch": 0.35,
            "dinner": 0.30,
            "snacks": 0.10
        }
        
        meal_calories = {
            meal: round(total_calories * percent, 1)
            for meal, percent in distribution.items()
        }
        
        return meal_calories
