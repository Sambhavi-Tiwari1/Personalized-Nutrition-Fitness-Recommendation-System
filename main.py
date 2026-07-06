#!/usr/bin/env python
"""
Main CLI Application
"""
import argparse
import yaml
import logging
import sys
from src.models.user import UserProfile
from src.calculators.bmr_calculator import BMRCalculator
from src.calculators.tdee_calculator import TDEECalculator
from src.calculators.macros_calculator import MacroCalculator
from src.recommendation.meal_planner import MealPlanner
from src.recommendation.workout_generator import WorkoutGenerator
from src.data.food_database import FoodDatabase
from src.data.exercise_database import ExerciseDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def interactive_mode():
    """Interactive CLI mode"""
    print("\n" + "="*60)
    print("🏋️ Welcome to Personalized Nutrition & Fitness Planner!")
    print("="*60 + "\n")
    
    # Get user inputs
    print("📝 Let's gather some information about you:\n")
    
    age = int(input("Age (years): "))
    gender = input("Gender (male/female): ").lower()
    weight = float(input("Weight (kg): "))
    height = float(input("Height (cm): "))
    
    print("\nActivity Level:")
    print("  1 - Sedentary (little or no exercise)")
    print("  2 - Lightly Active (1-3 days/week)")
    print("  3 - Moderately Active (3-5 days/week)")
    print("  4 - Very Active (6-7 days/week)")
    print("  5 - Extra Active (athlete/physical job)")
    activity_map = {"1": "sedentary", "2": "lightly_active", 
                    "3": "moderately_active", "4": "very_active", 
                    "5": "extra_active"}
    activity_choice = input("Select (1-5): ")
    activity_level = activity_map.get(activity_choice, "moderately_active")
    
    print("\nFitness Goal:")
    print("  1 - Fat Loss")
    print("  2 - Maintenance")
    print("  3 - Muscle Gain")
    goal_map = {"1": "fat_loss", "2": "maintenance", "3": "muscle_gain"}
    goal_choice = input("Select (1-3): ")
    goal = goal_map.get(goal_choice, "maintenance")
    
    print("\nDietary Preference:")
    print("  1 - Omnivore")
    print("  2 - Vegetarian")
    print("  3 - Vegan")
    print("  4 - Keto")
    print("  5 - Mediterranean")
    diet_map = {"1": "omnivore", "2": "vegetarian", "3": "vegan", 
                "4": "keto", "5": "mediterranean"}
    diet_choice = input("Select (1-5): ")
    dietary_preference = diet_map.get(diet_choice, "omnivore")
    
    allergies = input("\nAny food allergies? (comma separated, or 'none'): ")
    allergies = [] if allergies.lower() == "none" else [a.strip() for a in allergies.split(",")]
    
    experience = input("\nExperience Level (beginner/intermediate/advanced): ").lower()
    if experience not in ["beginner", "intermediate", "advanced"]:
        experience = "intermediate"
    
    days = input("Days per week to workout (1-7): ")
    days_per_week = int(days) if days.isdigit() and 1 <= int(days) <= 7 else 4
    
    # Create user profile
    user = UserProfile(
        age=age,
        gender=gender,
        weight=weight,
        height=height,
        activity_level=activity_level,
        goal=goal,
        dietary_preference=dietary_preference,
        allergies=allergies,
        experience_level=experience,
        days_per_week=days_per_week
    )
    
    # Generate plan
    generate_plan(user)

def generate_plan(user):
    """Generate and display plan"""
    print("\n" + "="*60)
    print("📊 YOUR PERSONALIZED PLAN")
    print("="*60)
    
    # Calculate BMR and TDEE
    bmr_calc = BMRCalculator()
    tdee_calc = TDEECalculator(bmr_calc)
    macro_calc = MacroCalculator()
    
    bmr = bmr_calc.calculate(user.weight, user.height, user.age, user.gender)
    tdee_data = tdee_calc.calculate(
        user.weight, user.height, user.age, user.gender,
        user.activity_level, user.goal
    )
    
    # Display metabolic metrics
    print("\n📐 BASIC METRICS")
    print("-"*40)
    print(f"  • BMR (Basal Metabolic Rate): {bmr:.0f} kcal/day")
    print(f"  • TDEE (Total Daily Energy Exp.): {tdee_data['tdee']:.0f} kcal/day")
    print(f"  • Goal: {user.goal.replace('_', ' ').title()}")
    print(f"  • Daily Calorie Target: {tdee_data['calorie_target']:.0f} kcal")
    print(f"  • Adjustment: {tdee_data['adjustment']:+.0f} kcal")
    
    # Calculate macros
    macros = macro_calc.calculate(user.weight, tdee_data["calorie_target"], user.goal)
    
    print("\n🥩 MACRONUTRIENT BREAKDOWN")
    print("-"*40)
    print(f"  • Protein: {macros['protein']['grams']:.0f}g ({macros['protein']['calories']:.0f} kcal) - {macros['protein']['percent']:.0f}%")
    print(f"  • Fats: {macros['fat']['grams']:.0f}g ({macros['fat']['calories']:.0f} kcal) - {macros['fat']['percent']:.0f}%")
    print(f"  • Carbs: {macros['carbs']['grams']:.0f}g ({macros['carbs']['calories']:.0f} kcal) - {macros['carbs']['percent']:.0f}%")
    
    # Generate meal plan
    food_db = FoodDatabase()
    meal_planner = MealPlanner(food_db)
    meal_plan = meal_planner.generate_plan(
        tdee_data["calorie_target"],
        macros,
        user.dietary_preference,
        user.allergies
    )
    
    print("\n🍽️ MEAL PLAN")
    print("-"*40)
    meals = ["breakfast", "lunch", "dinner", "snacks"]
    for meal_name in meals:
        meal = getattr(meal_plan, meal_name)
        print(f"\n{meal_name.title()} ({meal.percent:.0f}% - {meal.calories:.0f} kcal):")
        for item in meal.items:
            print(f"  • {item.name}: {item.quantity} ({item.calories:.0f} kcal)")
    
    # Generate workout plan
    exercise_db = ExerciseDatabase()
    workout_gen = WorkoutGenerator(exercise_db)
    workout_plan = workout_gen.generate_plan(
        user.goal,
        user.experience_level,
        user.days_per_week
    )
    
    print("\n🏋️ FITNESS PROGRAM")
    print("-"*40)
    print(f"Split: {workout_plan.split}")
    print(f"Days per week: {workout_plan.days_per_week}")
    
    for workout in workout_plan.workouts:
        print(f"\n{workout.name}:")
        for exercise in workout.exercises:
            print(f"  {exercise.sets} sets × {exercise.reps} reps - {exercise.name}")
    
    if workout_plan.cardio:
        print(f"\nCardio: {workout_plan.cardio.get('type', 'Recommended')}")
        print(f"  • Frequency: {workout_plan.cardio.get('frequency', '')}")
        print(f"  • Duration: {workout_plan.cardio.get('duration', '')}")
    
    print("\n💡 Recommendations:")
    print("-"*40)
    # Generate recommendations
    recommendations = generate_recommendations(user, tdee_data, macros)
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    print("\n" + "="*60)
    print("✅ Plan generated successfully!")
    print("="*60)

def generate_recommendations(user, tdee_data, macros):
    """Generate personalized recommendations"""
    recommendations = []
    
    if user.goal == "muscle_gain":
        recommendations.append(f"Increase protein intake to {macros['protein']['grams']:.0f}g daily")
        recommendations.append("Consume carbs around workout times")
    elif user.goal == "fat_loss":
        recommendations.append(f"Maintain high protein intake ({macros['protein']['grams']:.0f}g)")
        recommendations.append("Create a consistent calorie deficit")
    
    recommendations.append("Stay hydrated (2.5-3L water daily)")
    recommendations.append("Get 7-9 hours of quality sleep")
    recommendations.append("Track progress weekly")
    recommendations.append("Meal prep to stay consistent")
    
    return recommendations

def main():
    parser = argparse.ArgumentParser(description='Personalized Nutrition & Fitness Planner')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('--age', type=int, help='Age in years')
    parser.add_argument('--gender', type=str, choices=['male', 'female'], help='Gender')
    parser.add_argument('--weight', type=float, help='Weight in kg')
    parser.add_argument('--height', type=float, help='Height in cm')
    parser.add_argument('--activity', type=str, 
                       choices=['sedentary', 'lightly_active', 'moderately_active', 
                               'very_active', 'extra_active'],
                       help='Activity level')
    parser.add_argument('--goal', type=str, 
                       choices=['fat_loss', 'maintenance', 'muscle_gain'],
                       help='Fitness goal')
    parser.add_argument('--diet', type=str, default='omnivore',
                       help='Dietary preference')
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif all([args.age, args.gender, args.weight, args.height, args.activity, args.goal]):
        user = UserProfile(
            age=args.age,
            gender=args.gender,
            weight=args.weight,
            height=args.height,
            activity_level=args.activity,
            goal=args.goal,
            dietary_preference=args.diet
        )
        generate_plan(user)
    else:
        parser.print_help()
        print("\nPlease provide all required arguments or use --interactive mode")

if __name__ == "__main__":
    main()
