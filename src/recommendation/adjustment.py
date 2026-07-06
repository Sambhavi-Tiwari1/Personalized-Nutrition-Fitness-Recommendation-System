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
