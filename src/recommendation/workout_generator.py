"""
Workout Plan Generator
"""
import logging
import random
from typing import Dict, List, Optional
from ..data.exercise_database import ExerciseDatabase
from ..models.plan import Exercise, WorkoutDay, WorkoutPlan

logger = logging.getLogger(__name__)

class WorkoutGenerator:
    """
    Generate personalized workout plans
    """
    
    def __init__(self, exercise_db: Optional[ExerciseDatabase] = None):
        """
        Initialize workout generator
        """
        self.exercise_db = exercise_db or ExerciseDatabase()
        
        self.splits = {
            "push_pull_legs": {
                "name": "Push/Pull/Legs",
                "days": 6,
                "schedule": ["Push", "Pull", "Legs", "Push", "Pull", "Legs", "Rest"]
            },
            "upper_lower": {
                "name": "Upper/Lower",
                "days": 4,
                "schedule": ["Upper", "Lower", "Upper", "Lower", "Rest", "Rest", "Rest"]
            },
            "full_body": {
                "name": "Full Body",
                "days": 3,
                "schedule": ["Full Body", "Rest", "Full Body", "Rest", "Full Body", "Rest", "Rest"]
            }
        }
    
    def generate_plan(self, goal: str, experience_level: str = "intermediate",
                      days_per_week: int = 4, split_type: str = "upper_lower") -> WorkoutPlan:
        """
        Generate complete workout plan
        
        Args:
            goal: Fitness goal
            experience_level: Beginner/Intermediate/Advanced
            days_per_week: Training frequency
            split_type: Type of workout split
            
        Returns:
            Complete workout plan
        """
        # Select appropriate split
        if split_type not in self.splits:
            split_type = "upper_lower"
        
        split = self.splits[split_type]
        
        # Adjust based on days per week
        days = split["schedule"][:days_per_week + 1]
        
        # Generate workouts for each day
        workouts = []
        for day, day_name in enumerate(days):
            if day_name == "Rest":
                continue
            
            exercises = self._select_exercises(
                day_name, goal, experience_level
            )
            
            workouts.append(WorkoutDay(
                day=day + 1,
                name=f"Day {day + 1}: {day_name}",
                exercises=exercises,
                notes=self._get_day_notes(day_name, goal)
            ))
        
        return WorkoutPlan(
            split=split["name"],
            days_per_week=len([d for d in days if d != "Rest"]),
            workouts=workouts,
            cardio=self._get_cardio_suggestions(goal),
            warmup=self._get_warmup(),
            cooldown=self._get_cooldown()
        )
    
    def _select_exercises(self, day_type: str, goal: str,
                          experience_level: str) -> List[Exercise]:
        """
        Select exercises for a workout day
        """
        if day_type == "Push":
            muscles = ["chest", "shoulders", "triceps"]
            count = 6
        elif day_type == "Pull":
            muscles = ["back", "biceps", "rear_delts"]
            count = 6
        elif day_type == "Legs":
            muscles = ["quadriceps", "hamstrings", "glutes", "calves"]
            count = 6
        elif day_type == "Upper":
            muscles = ["chest", "back", "shoulders", "biceps", "triceps"]
            count = 8
        elif day_type == "Lower":
            muscles = ["quadriceps", "hamstrings", "glutes", "calves"]
            count = 6
        else:  # Full Body
            muscles = ["chest", "back", "shoulders", "legs", "core"]
            count = 8
        
        # Get exercises for each muscle
        selected = []
        
        for muscle in muscles:
            exercises = self.exercise_db.get_exercises_by_muscle(
                muscle, experience_level
            )
            
            if exercises:
                # Add 1-2 exercises per muscle
                num_exercises = min(2, count // len(muscles) + 1)
                for _ in range(num_exercises):
                    if exercises:
                        ex = random.choice(exercises)
                        selected.append(self._create_exercise(ex, goal, experience_level))
                        exercises.remove(ex)
        
        # Shuffle and limit
        random.shuffle(selected)
        selected = selected[:count]
        
        return selected
    
    def _create_exercise(self, exercise: Dict, goal: str,
                         experience_level: str) -> Exercise:
        """Create Exercise object"""
        # Determine sets and reps based on goal
        if goal == "muscle_gain":
            sets = 3 if experience_level == "beginner" else 4
            reps = "8-12"
        elif goal == "fat_loss":
            sets = 3
            reps = "12-15"
        else:  # maintenance
            sets = 3
            reps = "10-12"
        
        return Exercise(
            name=exercise.get('name', 'Unknown'),
            sets=sets,
            reps=reps,
            rest="60-90s",
            notes=exercise.get('notes', '')
        )
    
    def _get_day_notes(self, day_type: str, goal: str) -> str:
        """Get workout day notes"""
        notes = {
            "Push": "Focus on progressive overload for chest and shoulders",
            "Pull": "Maintain proper form on pulling movements",
            "Legs": "Warm up properly before heavy squats",
            "Upper": "Balance pushing and pulling exercises",
            "Lower": "Include both compound and isolation exercises",
            "Full Body": "Prioritize compound movements"
        }
        
        base_note = notes.get(day_type, "Focus on proper form")
        
        if goal == "muscle_gain":
            return base_note + ". Aim for 8-12 reps with progressive overload."
        elif goal == "fat_loss":
            return base_note + ". Keep rest periods short (45-60s)."
        else:
            return base_note + ". Maintain intensity with good form."
    
    def _get_warmup(self) -> str:
        """Get warmup routine"""
        return """5-10 minutes light cardio (jumping jacks, jogging, cycling)
Dynamic stretching: arm circles, leg swings, torso twists
Specific warm-up sets for compound exercises (2-3 light sets)"""
    
    def _get_cooldown(self) -> str:
        """Get cooldown routine"""
        return """5-10 minutes light cardio to lower heart rate
Static stretching: hold each stretch for 15-30 seconds
Focus on muscles worked during the workout"""
    
    def _get_cardio_suggestions(self, goal: str) -> Dict[str, str]:
        """Get cardio suggestions based on goal"""
        if goal == "fat_loss":
            return {
                "type": "HIIT (High-Intensity Interval Training)",
                "frequency": "3-4 times per week",
                "duration": "15-20 minutes",
                "examples": "Sprinting, Burpees, Jump Rope, Cycling"
            }
        elif goal == "maintenance":
            return {
                "type": "LISS (Low-Intensity Steady State)",
                "frequency": "2-3 times per week",
                "duration": "30-45 minutes",
                "examples": "Walking, Jogging, Cycling, Swimming"
            }
        else:  # muscle_gain
            return {
                "type": "Moderate Intensity Steady State",
                "frequency": "2-3 times per week",
                "duration": "20-30 minutes",
                "examples": "Walking, Light Jogging, Cycling"
            }
