"""
Meal Plan Generator
"""
import logging
import random
from typing import Dict, List, Optional
from ..data.food_database import FoodDatabase
from ..models.plan import Meal, FoodItem, MealPlan

logger = logging.getLogger(__name__)

class MealPlanner:
    """
    Generate personalized meal plans
    """
    
    def __init__(self, food_db: Optional[FoodDatabase] = None):
        """
        Initialize meal planner
        """
        self.food_db = food_db or FoodDatabase()
        self.meal_distribution = {
            "breakfast": 0.25,
            "lunch": 0.35,
            "dinner": 0.30,
            "snacks": 0.10
        }
    
    def generate_plan(self, total_calories: float, macros: Dict,
                      dietary_preference: str = "omnivore",
                      allergies: List[str] = None) -> MealPlan:
        """
        Generate complete meal plan
        
        Args:
            total_calories: Daily calorie target
            macros: Macronutrient targets
            dietary_preference: Diet type
            allergies: Food allergies
            
        Returns:
            Complete meal plan
        """
        allergies = allergies or []
        
        # Get meal calorie targets
        meal_calories = {
            meal: round(total_calories * percent, 1)
            for meal, percent in self.meal_distribution.items()
        }
        
        # Get foods for each meal
        meals = {}
        for meal_name, calories in meal_calories.items():
            foods = self._select_foods(
                meal_name, calories, macros,
                dietary_preference, allergies
            )
            meals[meal_name] = foods
        
        return MealPlan(
            breakfast=self._create_meal("Breakfast", meals["breakfast"], 
                                       self.meal_distribution["breakfast"]),
            lunch=self._create_meal("Lunch", meals["lunch"],
                                   self.meal_distribution["lunch"]),
            dinner=self._create_meal("Dinner", meals["dinner"],
                                    self.meal_distribution["dinner"]),
            snacks=self._create_meal("Snacks", meals["snacks"],
                                    self.meal_distribution["snacks"]),
            total_calories=total_calories
        )
    
    def _select_foods(self, meal_type: str, calories: float,
                     macros: Dict, diet: str, allergies: List[str]) -> List[Dict]:
        """
        Select appropriate foods for a meal
        """
        # Get foods for this meal type
        foods = self.food_db.get_foods_by_meal(meal_type, diet, allergies)
        
        if not foods:
            # Fallback to general foods
            foods = self.food_db.get_foods_by_meal(meal_type, "omnivore", allergies)
        
        # Select foods to meet calorie target
        selected = []
        remaining_calories = calories
        
        # Sort by food type (protein, carbs, fats)
        protein_foods = [f for f in foods if f.get('protein_ratio', 0) > 0.3]
        carb_foods = [f for f in foods if f.get('carb_ratio', 0) > 0.4]
        fat_foods = [f for f in foods if f.get('fat_ratio', 0) > 0.4]
        
        # Add protein
        if protein_foods and remaining_calories > 0:
            food = random.choice(protein_foods[:5])
            amount = self._calculate_amount(food, remaining_calories * 0.35)
            selected.append(self._create_food_item(food, amount))
            remaining_calories -= amount * food.get('calories_per_100g', 0) / 100
        
        # Add carbs
        if carb_foods and remaining_calories > 0:
            food = random.choice(carb_foods[:5])
            amount = self._calculate_amount(food, remaining_calories * 0.5)
            selected.append(self._create_food_item(food, amount))
            remaining_calories -= amount * food.get('calories_per_100g', 0) / 100
        
        # Add fats
        if fat_foods and remaining_calories > 0:
            food = random.choice(fat_foods[:3])
            amount = self._calculate_amount(food, remaining_calories)
            selected.append(self._create_food_item(food, amount))
        
        # Ensure minimum calories
        if calories > 0 and not selected:
            # Add a default food
            default_food = foods[0] if foods else {
                'name': 'Mixed Greens',
                'calories_per_100g': 20,
                'protein_per_100g': 1,
                'carbs_per_100g': 3,
                'fat_per_100g': 0
            }
            amount = self._calculate_amount(default_food, calories)
            selected.append(self._create_food_item(default_food, amount))
        
        return selected
    
    def _calculate_amount(self, food: Dict, target_calories: float) -> float:
        """Calculate food amount to meet calorie target"""
        calories_per_100g = food.get('calories_per_100g', 100)
        if calories_per_100g <= 0:
            return 100
        return round((target_calories / calories_per_100g) * 100, 1)
    
    def _create_food_item(self, food: Dict, amount: float) -> FoodItem:
        """Create FoodItem from food data and amount"""
        calories_per_100g = food.get('calories_per_100g', 0)
        protein = food.get('protein_per_100g', 0)
        carbs = food.get('carbs_per_100g', 0)
        fat = food.get('fat_per_100g', 0)
        
        factor = amount / 100
        
        return FoodItem(
            name=food.get('name', 'Unknown'),
            quantity=f"{amount}g",
            calories=round(calories_per_100g * factor, 1),
            protein=round(protein * factor, 1),
            carbs=round(carbs * factor, 1),
            fat=round(fat * factor, 1)
        )
    
    def _create_meal(self, name: str, items: List[Dict], 
                     percent: float) -> Meal:
        """Create Meal object"""
        total_calories = sum(item.calories for item in items)
        
        return Meal(
            name=name,
            calories=round(total_calories, 1),
            percent=round(percent * 100, 1),
            items=items
        )
