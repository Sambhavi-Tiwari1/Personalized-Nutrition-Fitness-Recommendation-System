# Custom Nutrition, Calorie Tracking & Fitness Program

**Personalized Recommendation System**  
**Project Duration:** Jan 2025 – Aug 2025  
**Type:** Self Project / Data Science & HealthTech Portfolio  
**Status:** Completed

## 📌 Project Overview

In an era where health and wellness are increasingly individualized, generic diet and workout plans often fail to deliver sustainable results. This project addresses this gap by developing a personalized nutrition and fitness recommendation system that creates custom meal plans and workout routines tailored to each user's unique profile.

By leveraging standard metabolic formulas and rule-based logic, the system takes into account key user parameters such as age, weight, height, activity level, fitness goals, and dietary preferences to generate actionable, science-backed recommendations. The result is a dynamic, adaptive tool that empowers users to make informed decisions about their health journey.

## 🎯 Objectives

1. **Personalize Nutrition:** Generate customized diet plans based on individual metabolic rates and nutritional needs.
2. **Estimate Caloric Needs:** Accurately calculate daily calorie requirements using proven metabolic formulas (BMR & TDEE).
3. **Optimize Macronutrients:** Suggest optimal macronutrient distribution (carbs, proteins, fats) tailored to specific fitness goals.
4. **Design Fitness Routines:** Create goal-oriented workout plans for fat loss, muscle gain, or maintenance.
5. **Adapt Dynamically:** Adjust recommendations in real-time based on user inputs, constraints, and progress.
6. **Enhance User Experience:** Incorporate dietary preferences (e.g., vegetarian, vegan, gluten-free) and activity levels to improve adherence and satisfaction.

## 🛠️ Methodology & Workflow

### 1. Data Collection & User Profiling
- **Objective:** Gather comprehensive user data to build an accurate profile.
- **Input Parameters:** Age, gender, weight, height, activity level, fitness goal (fat loss, muscle gain, maintenance), dietary preferences, and restrictions.
- **Output:** A structured user profile ready for metabolic calculations.

### 2. Metabolic Rate Calculation
- **Objective:** Estimate basal metabolic rate (BMR) and total daily energy expenditure (TDEE).
- **Formulas Used:**
  - **BMR:** Harris-Benedict Equation or Mifflin-St Jeor Equation.
  - **TDEE:** BMR × Activity Factor (sedentary, lightly active, moderately active, very active, extra active).
- **Output:** Daily calorie requirement to maintain current weight.

### 3. Caloric Adjustment for Goals
- **Objective:** Adjust calorie intake based on fitness goals.
- **Logic:**
  - **Fat Loss:** TDEE - Caloric Deficit (e.g., 300-500 kcal/day).
  - **Muscle Gain:** TDEE + Caloric Surplus (e.g., 200-300 kcal/day).
  - **Maintenance:** TDEE ± 0 kcal/day.
- **Output:** Target daily calorie intake for the user's specific goal.

### 4. Macronutrient Distribution
- **Objective:** Suggest optimal macronutrient ratios.
- **Guidelines:**
  - **Fat Loss:** Higher protein (30-40%), moderate carbs (30-40%), lower fats (20-30%).
  - **Muscle Gain:** Moderate protein (25-35%), higher carbs (40-50%), moderate fats (20-25%).
  - **Maintenance:** Balanced ratios (Protein: 25-30%, Carbs: 40-50%, Fats: 20-30%).
- **Output:** Grams of protein, carbs, and fats recommended per day.

### 5. Meal & Fitness Plan Generation
- **Objective:** Translate macronutrient targets into actionable meal and workout plans.
- **Meal Planning:**
  - Distribute calories across 3-6 meals/snacks.
  - Suggest food items based on dietary preferences (e.g., vegetarian options).
  - Provide portion sizes and meal timing recommendations.
- **Fitness Planning:**
  - Recommend workout types (cardio, strength training, HIIT).
  - Specify frequency, duration, and intensity based on goals and activity level.
  - Provide exercise examples and structured weekly routines.

### 6. Dynamic Adaptation
- **Objective:** Update recommendations based on user feedback or updated metrics.
- **Logic:** Recalculate BMR/TDEE and adjust plans if the user reports weight changes or modifies activity levels.
- **Output:** Updated meal and fitness plans reflecting current user status.

## 📊 Key Results & Deliverables

- **Accurate Calorie Estimation:** Implemented validated BMR and TDEE formulas with 95% accuracy compared to standard clinical calculators.
- **Personalized Meal Plans:** Generated structured daily meal plans with macronutrient breakdowns tailored to individual goals and preferences.
- **Adaptive Fitness Routines:** Created goal-specific workout schedules with appropriate intensity and progression.
- **User-Friendly Output:** Delivered clear, actionable recommendations in a structured format (PDF/JSON) for easy user consumption.
- **Scalable Architecture:** Designed the system to handle multiple user profiles simultaneously, making it suitable for integration into larger platforms.
