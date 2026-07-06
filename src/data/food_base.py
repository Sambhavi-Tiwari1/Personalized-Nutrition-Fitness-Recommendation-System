"""
Food Database
"""
import pandas as pd
import logging
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class FoodDatabase:
    """
    Food nutrition database
    """
    
    def __init__(self, db_path: str = "data/food_data.csv"):
        """
        Initialize food database
        """
        self.db_path = db_path
        self.foods = self._load_database()
        
    def _load_database(self) -> pd.DataFrame:
        """Load food database from CSV"""
        if Path(self.db_path).exists():
            df = pd.read_csv(self.db_path)
        else:
            # Create sample database
            df = self._create_sample_database()
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(self.db_path, index=False)
        
        return df
    
    def _create_sample_database(self) -> pd.DataFrame:
        """Create sample food database"""
        data = [
            # Breakfast foods
            {"name": "Oatmeal", "meal_type": "breakfast", "calories_per_100g": 389, 
             "protein_per_100g": 13, "carbs_per_100g": 66, "fat_per_100g": 7},
            {"name": "Skim Milk", "meal_type": "breakfast", "calories_per_100g": 36, 
             "protein_per_100g": 3.6, "carbs_per_100g": 5, "fat_per_100g": 0.1},
            {"name": "Bananas", "meal_type": "breakfast", "calories_per_100g": 105, 
             "protein_per_100g": 1.3, "carbs_per_100g": 27, "fat_per_100g": 0.3},
            {"name": "Almonds", "meal_type": "breakfast", "calories_per_100g": 579, 
             "protein_per_100g": 21, "carbs_per_100g": 22, "fat_per_100g": 49},
            {"name": "Honey", "meal_type": "breakfast", "calories_per_100g": 304, 
             "protein_per_100g": 0.3, "carbs_per_100g": 82, "fat_per_100g": 0},
            {"name": "Greek Yogurt", "meal_type": "breakfast", "calories_per_100g": 60, 
             "protein_per_100g": 10, "carbs_per_100g": 3, "fat_per_100g": 0.4},
            
            # Lunch/Dinner foods
            {"name": "Grilled Chicken Breast", "meal_type": "lunch", "calories_per_100g": 165, 
             "protein_per_100g": 31, "carbs_per_100g": 0, "fat_per_100g": 3.6},
            {"name": "Brown Rice", "meal_type": "lunch", "calories_per_100g": 123, 
             "protein_per_100g": 3, "carbs_per_100g": 26, "fat_per_100g": 0.9},
            {"name": "Broccoli", "meal_type": "lunch", "calories_per_100g": 34, 
             "protein_per_100g": 2.8, "carbs_per_100g": 7, "fat_per_100g": 0.4},
            {"name": "Sweet Potato", "meal_type": "lunch", "calories_per_100g": 90, 
             "protein_per_100g": 2, "carbs_per_100g": 21, "fat_per_100g": 0.1},
            {"name": "Olive Oil", "meal_type": "lunch", "calories_per_100g": 884, 
             "protein_per_100g": 0, "carbs_per_100g": 0, "fat_per_100g": 100},
            {"name": "Avocado", "meal_type": "lunch", "calories_per_100g": 160, 
             "protein_per_100g": 2, "carbs_per_100g": 9, "fat_per_100g": 15},
            {"name": "Salmon Fillet", "meal_type": "dinner", "calories_per_100g": 208, 
             "protein_per_100g": 22, "carbs_per_100g": 0, "fat_per_100g": 13},
            {"name": "Quinoa", "meal_type": "dinner", "calories_per_100g": 120, 
             "protein_per_100g": 4.4, "carbs_per_100g": 21, "fat_per_100g": 1.9},
            {"name": "Asparagus", "meal_type": "dinner", "calories_per_100g": 20, 
             "protein_per_100g": 2.2, "carbs_per_100g": 4, "fat_per_100g": 0.1},
            {"name": "Butter", "meal_type": "dinner", "calories_per_100g": 717, 
             "protein_per_100g": 0.9, "carbs_per_100g": 0.1, "fat_per_100g": 81},
            {"name": "Parmesan Cheese", "meal_type": "dinner", "calories_per_100g": 431, 
             "protein_per_100g": 38, "carbs_per_100g": 1, "fat_per_100g": 29},
            
            # Snacks
            {"name": "Apple", "meal_type": "snack", "calories_per_100g": 52, 
             "protein_per_100g": 0.3, "carbs_per_100g": 14, "fat_per_100g": 0.2},
            {"name": "Peanut Butter", "meal_type": "snack", "calories_per_100g": 588, 
             "protein_per_100g": 25, "carbs_per_100g": 20, "fat_per_100g": 50},
            {"name": "Protein Bar", "meal_type": "snack", "calories_per_100g": 350, 
             "protein_per_100g": 30, "carbs_per_100g": 35, "fat_per_100g": 10},
        ]
        
        return pd.DataFrame(data)
    
    def get_foods_by_meal(self, meal_type: str, 
                         dietary_preference: str = "omnivore",
                         allergies: List[str] = None) -> List[Dict]:
        """
        Get foods for a specific meal type
        """
        allergies = allergies or []
        
        # Filter by meal type
        foods = self.foods[self.foods['meal_type'] == meal_type]
        
        # Convert to list of dictionaries
        foods_list = foods.to_dict('records')
        
        return foods_list
    
    def search_foods(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for foods by name
        """
        mask = self.foods['name'].str.contains(query, case=False, na=False)
        results = self.foods[mask].head(limit)
        return results.to_dict('records')
