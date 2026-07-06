"""
Real-time Plan Adjustments
"""
import logging
from typing import Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PlanAdjuster:
    """
    Adjust plans based on progress and feedback
    """
    
    def __init__(self):
        self.adjustment_factors = {
            "weight_loss": {
                "slow": 0.9,    # Decrease calories by 10%
                "fast": 1.1,    # Increase calories by 10%
                "target": 0.5   # 0.5 kg/week target
            },
            "muscle_gain": {
                "slow": 1.1,    # Increase calories by 10%
                "fast": 0.9,    # Decrease calories by 10%
                "target": 0.25  # 0.25 kg/week target
            }
        }
    
    def adjust_calories(self, current_calories: float, weight_change: float,
                        weeks: int, goal: str) -> Dict[str, float]:
        """
        Adjust calorie target based on progress
        
        Args:
            current_calories: Current daily calories
            weight_change: Total weight change (kg)
            weeks: Number of weeks
            goal: Fitness goal
            
        Returns:
            Adjusted calorie target
        """
        # Calculate weekly weight change
        weekly_change = weight_change / max(weeks, 1)
        
        # Get target based on goal
        if goal == "fat_loss":
            target = 0.5  # kg/week (healthy fat loss)
            adjustment_factor = self.adjustment_factors["weight_loss"]
        elif goal == "muscle_gain":
            target = 0.25  # kg/week (healthy muscle gain)
            adjustment_factor = self.adjustment_factors["muscle_gain"]
        else:  # maintenance
            return {"adjusted_calories": current_calories, "adjustment": 0}
        
        # Determine adjustment
        if weekly_change < target * 0.8:
            # Too slow - increase deficit or surplus
            factor = adjustment_factor["slow"]
            adjustment = current_calories * (factor - 1)
        elif weekly_change > target * 1.2:
            # Too fast - decrease deficit or surplus
            factor = adjustment_factor["fast"]
            adjustment = current_calories * (factor - 1)
        else:
            # On track
            adjustment = 0
        
        adjusted_calories = round(current_calories + adjustment, 1)
        
        logger.info(f"Calorie adjustment: {adjustment:.1f} kcal -> {adjusted_calories:.1f} kcal")
        
        return {
            "adjusted_calories": adjusted_calories,
            "adjustment": round(adjustment, 1),
            "weekly_change": round(weekly_change, 3),
            "target": target
        }
    
    def adjust_macros(self, current_macros: Dict, calorie_change: float,
                      weight_kg: float) -> Dict:
        """
        Adjust macronutrients based on calorie change
        """
        from ..calculators.macros_calculator import MacroCalculator
        
        calculator = MacroCalculator()
        new_calories = current_macros['total_calories'] + calorie_change
        
        # Recalculate macros
        new_macros = calculator.calculate(weight_kg, new_calories, 
                                         current_macros.get('goal', 'maintenance'))
        
        # Add total calories to result
        new_macros['total_calories'] = new_calories
        
        return new_macros
    
    def adjust_exercise_intensity(self, current_plan: Dict, 
                                  progress: float,
                                  weeks: int) -> Dict:
        """
        Adjust workout intensity based on progress
        """
        # Calculate progress per week
        weekly_progress = progress / max(weeks, 1)
        
        # Determine intensity adjustment
        if weekly_progress > 0.1:  # Good progress
            intensity_factor = 1.1  # Increase intensity by 10%
        elif weekly_progress > 0.05:  # Moderate progress
            intensity_factor = 1.05  # Increase intensity by 5%
        else:  # Slow progress
            intensity_factor = 0.95  # Decrease intensity by 5%
        
        adjusted_plan = current_plan.copy()
        
        # Adjust sets and reps
        for workout in adjusted_plan.get('workouts', []):
            for exercise in workout.get('exercises', []):
                if exercise.get('sets', 0) > 0:
                    exercise['sets'] = int(exercise['sets'] * intensity_factor)
                if exercise.get('reps', ''):
                    reps_range = exercise['reps'].split('-')
                    if len(reps_range) == 2:
                        new_reps_lower = int(float(reps_range[0]) * intensity_factor)
                        new_reps_upper = int(float(reps_range[1]) * intensity_factor)
                        exercise['reps'] = f"{new_reps_lower}-{new_reps_upper}"
        
        return adjusted_plan
    
    def get_plan_adjustments(self, current_plan: Dict,
                            progress_data: Dict,
                            weeks: int) -> Dict:
        """
        Get comprehensive plan adjustments
        """
        adjustments = {
            "timestamp": datetime.now().isoformat(),
            "calories": None,
            "macros": None,
            "workout": None,
            "recommendations": []
        }
        
        # Adjust calories
        if 'weight_change' in progress_data:
            cal_adjustment = self.adjust_calories(
                current_plan.get('calorie_target', 0),
                progress_data['weight_change'],
                weeks,
                current_plan.get('goal', 'maintenance')
            )
            adjustments['calories'] = cal_adjustment
        
        # Adjust macros if calories changed
        if adjustments['calories'] and adjustments['calories']['adjustment'] != 0:
            macro_adjustment = self.adjust_macros(
                current_plan.get('macros', {}),
                adjustments['calories']['adjustment'],
                current_plan.get('weight', 70)
            )
            adjustments['macros'] = macro_adjustment
        
        # Adjust workout
        if 'performance' in progress_data:
            workout_adjustment = self.adjust_exercise_intensity(
                current_plan.get('workout_plan', {}),
                progress_data['performance'],
                weeks
            )
            adjustments['workout'] = workout_adjustment
        
        # Generate recommendations
        adjustments['recommendations'] = self._generate_recommendations(
            adjustments, progress_data
        )
        
        return adjustments
    
    def _generate_recommendations(self, adjustments: Dict,
                                  progress: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if adjustments.get('calories'):
            cal = adjustments['calories']
            if cal['adjustment'] < 0:
                recommendations.append("Consider reducing calorie intake by 100-200 calories per day")
            elif cal['adjustment'] > 0:
                recommendations.append("Consider increasing calorie intake by 100-200 calories per day")
        
        if 'weight_change' in progress:
            weight_change = progress['weight_change']
            weeks = progress.get('weeks', 1)
            weekly_change = weight_change / weeks
            
            if weekly_change > 0.5 and progress.get('goal') == 'fat_loss':
                recommendations.append("Weight loss is very rapid. Ensure adequate nutrition.")
            elif weekly_change < 0.1 and progress.get('goal') == 'muscle_gain':
                recommendations.append("Muscle gain is slow. Increase calorie surplus slightly.")
        
        if progress.get('adherence', 0) < 0.7:
            recommendations.append("Focus on consistency. Track your daily intake and activity.")
        
        return recommendations
