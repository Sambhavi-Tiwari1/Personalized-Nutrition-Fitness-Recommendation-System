# Personalized-Nutrition-Fitness-Recommendation-System

An intelligent, personalized nutrition and fitness recommendation system that generates customized diet and workout plans based on user-specific data, goals, and preferences using BMR/TDEE calculations and rule-based engines.

Features • How It Works • Installation • Usage • API Endpoints • Project Structure

📊 Overview
This project implements a comprehensive personalized recommendation system that generates custom nutrition and fitness plans using standard metabolic formulas (BMR, TDEE) and a sophisticated rule-based engine. It considers user-specific data including age, weight, height, activity level, fitness goals, and dietary preferences to create truly personalized recommendations.

🧮 How It Works
Core Calculation Pipeline

┌─────────────────────────────────────────────────────────────────┐
│                     USER INPUT                                 │
│  • Age, Gender, Height, Weight                                 │
│  • Activity Level (Sedentary to Extra Active)                 │
│  • Fitness Goal (Fat Loss, Maintenance, Muscle Gain)         │
│  • Dietary Preferences                                         │
│  • Allergies/Food Restrictions                                 │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BMR CALCULATION                             │
│  Mifflin-St Jeor Equation                                     │
│  BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(y) + s  │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    TDEE CALCULATION                            │
│  TDEE = BMR × Activity Factor                                 │
│  Sedentary: 1.2  |  Light: 1.375  |  Moderate: 1.55          │
│  Active: 1.725  |  Extra Active: 1.9                         │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                GOAL-BASED CALORIE ADJUSTMENT                   │
│  • Fat Loss: TDEE - 500 calories/day                         │
│  • Maintenance: TDEE                                          │
│  • Muscle Gain: TDEE + 300 calories/day                      │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│              MACRONUTRIENT DISTRIBUTION                        │
│  • Protein: 1.6-2.2g/kg body weight                          │
│  • Fats: 20-35% of total calories                            │
│  • Carbs: Remaining calories                                  │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│           MEAL PLAN GENERATION                                 │
│  • Breakfast, Lunch, Dinner, Snacks                          │
│  • Calorie distribution: 25%, 35%, 30%, 10%                  │
│  • Food suggestions based on preferences                     │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│         FITNESS PROGRAM GENERATION                             │
│  • Goal-specific workouts                                     │
│  • Exercise selection and sequencing                          │
│  • Sets, reps, and intensity recommendations                 │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│              COMPLETE PERSONALIZED PLAN                        │
│  • Daily calorie target                                        │
│  • Macronutrient breakdown                                     │
│  • Meal plan with portion sizes                                │
│  • Exercise routine with progression                          │
└─────────────────────────────────────────────────────────────────┘
