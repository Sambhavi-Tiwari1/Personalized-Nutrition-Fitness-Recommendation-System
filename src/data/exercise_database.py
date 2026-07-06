"""
Exercise Database
"""
import pandas as pd
import logging
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class ExerciseDatabase:
    """
    Exercise database
    """
    
    def __init__(self, db_path: str = "data/exercise_data.csv"):
        """
        Initialize exercise database
        """
        self.db_path = db_path
        self.exercises = self._load_database()
        
    def _load_database(self) -> pd.DataFrame:
        """Load exercise database from CSV"""
        if Path(self.db_path).exists():
            df = pd.read_csv(self.db_path)
        else:
            df = self._create_sample_database()
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(self.db_path, index=False)
        
        return df
    
    def _create_sample_database(self) -> pd.DataFrame:
        """Create sample exercise database"""
        data = [
            # Chest
            {"name": "Bench Press", "muscle": "chest", "level": "intermediate",
             "notes": "Keep shoulders pinned back and down"},
            {"name": "Incline Dumbbell Press", "muscle": "chest", "level": "intermediate",
             "notes": "Focus on upper chest"},
            {"name": "Push-ups", "muscle": "chest", "level": "beginner",
             "notes": "Keep body straight"},
            {"name": "Cable Flyes", "muscle": "chest", "level": "advanced",
             "notes": "Control the weight throughout"},
            
            # Back
            {"name": "Deadlifts", "muscle": "back", "level": "advanced",
             "notes": "Maintain neutral spine"},
            {"name": "Pull-ups", "muscle": "back", "level": "intermediate",
             "notes": "Full range of motion"},
            {"name": "Seated Cable Rows", "muscle": "back", "level": "intermediate",
             "notes": "Squeeze shoulder blades together"},
            {"name": "Face Pulls", "muscle": "back", "level": "beginner",
             "notes": "Focus on external rotation"},
            
            # Shoulders
            {"name": "Overhead Press", "muscle": "shoulders", "level": "intermediate",
             "notes": "Stabilize core"},
            {"name": "Dumbbell Lateral Raises", "muscle": "shoulders", "level": "beginner",
             "notes": "Slight bend in elbows"},
            {"name": "Front Raises", "muscle": "shoulders", "level": "beginner",
             "notes": "Controlled movement"},
            {"name": "Rear Delt Flyes", "muscle": "shoulders", "level": "intermediate",
             "notes": "Focus on rear deltoids"},
            
            # Legs
            {"name": "Squats", "muscle": "legs", "level": "intermediate",
             "notes": "Go below parallel"},
            {"name": "Romanian Deadlifts", "muscle": "legs", "level": "intermediate",
             "notes": "Keep back straight"},
            {"name": "Leg Press", "muscle": "legs", "level": "beginner",
             "notes": "Full range of motion"},
            {"name": "Leg Curls", "muscle": "legs", "level": "beginner",
             "notes": "Control the negative"},
            {"name": "Leg Extensions", "muscle": "legs", "level": "beginner",
             "notes": "Full extension"},
            {"name": "Calf Raises", "muscle": "legs", "level": "beginner",
             "notes": "Full range of motion"},
            
            # Arms
            {"name": "Barbell Curls", "muscle": "biceps", "level": "intermediate",
             "notes": "Keep elbows pinned"},
            {"name": "Hammer Curls", "muscle": "biceps", "level": "beginner",
             "notes": "Neutral grip"},
            {"name": "Tricep Pushdowns", "muscle": "triceps", "level": "beginner",
             "notes": "Keep elbows tucked"},
            {"name": "Skull Crushers", "muscle": "triceps", "level": "intermediate",
             "notes": "Control the weight"},
            {"name": "Overhead Tricep Extensions", "muscle": "triceps", "level": "intermediate",
             "notes": "Full extension"},
            
            # Core
            {"name": "Planks", "muscle": "core", "level": "beginner",
             "notes": "Keep body straight"},
            {"name": "Leg Raises", "muscle": "core", "level": "intermediate",
             "notes": "Keep lower back pressed down"},
            {"name": "Crunches", "muscle": "core", "level": "beginner",
             "notes": "Controlled movement"},
            {"name": "Russian Twists", "muscle": "core", "level": "intermediate",
             "notes": "Rotate through full range"},
        ]
        
        return pd.DataFrame(data)
    
    def get_exercises_by_muscle(self, muscle: str, 
                               experience_level: str = "intermediate") -> List[Dict]:
        """
        Get exercises for a specific muscle group
        """
        # Filter by muscle and experience level
        exercises = self.exercises[
            (self.exercises['muscle'] == muscle) |
            (self.exercises['muscle'] == 'legs' and muscle in ['quadriceps', 'hamstrings', 'glutes', 'calves'])
        ]
        
        # Filter by experience level
        levels = {
            "beginner": ["beginner"],
            "intermediate": ["beginner", "intermediate"],
            "advanced": ["beginner", "intermediate", "advanced"]
        }
        
        allowed_levels = levels.get(experience_level, ["beginner", "intermediate"])
        exercises = exercises[exercises['level'].isin(allowed_levels)]
        
        return exercises.to_dict('records')
