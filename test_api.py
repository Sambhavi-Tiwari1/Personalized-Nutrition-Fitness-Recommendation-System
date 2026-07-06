"""
API Testing Script
"""
import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health: {response.json()}")
    return response.status_code == 200

def test_generate_plan():
    """Test plan generation"""
    data = {
        "age": 28,
        "gender": "male",
        "weight": 72,
        "height": 175,
        "activity_level": "moderately_active",
        "goal": "muscle_gain",
        "dietary_preference": "omnivore",
        "allergies": [],
        "experience_level": "intermediate",
        "days_per_week": 4
    }
    
    start_time = time.time()
    response = requests.post(f"{BASE_URL}/plan/generate", json=data)
    elapsed = time.time() - start_time
    
    print(f"\nPlan Generation: {elapsed:.2f}s")
    
    if response.status_code == 200:
        plan = response.json()
        print(f"  ✅ Plan generated successfully")
        print(f"  • Calorie Target: {plan['metabolic_metrics']['calorie_target']}")
        print(f"  • Meals: {len(plan['meal_plan'])}")
        print(f"  • Workouts: {len(plan['workout_plan']['workouts'])}")
        print(f"  • Recommendations: {len(plan['recommendations'])}")
        return True
    else:
        print(f"  ❌ Error: {response.text}")
        return False

def test_nutrition_calculation():
    """Test nutrition calculation"""
    data = {
        "age": 28,
        "gender": "male",
        "weight": 72,
        "height": 175,
        "activity_level": "moderately_active",
        "goal": "muscle_gain"
    }
    
    response = requests.post(f"{BASE_URL}/nutrition/calculate", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nNutrition Calculation:")
        print(f"  • BMR: {result['bmr']:.0f} kcal")
        print(f"  • TDEE: {result['tdee']:.0f} kcal")
        print(f"  • Calorie Target: {result['calorie_target']:.0f} kcal")
        return True
    else:
        print(f"  ❌ Error: {response.text}")
        return False

def test_workout_generation():
    """Test workout generation"""
    data = {
        "goal": "muscle_gain",
        "experience_level": "intermediate",
        "days_per_week": 4
    }
    
    response = requests.post(f"{BASE_URL}/workout/generate", json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nWorkout Generation:")
        print(f"  • Split: {result['split']}")
        print(f"  • Days: {result['days_per_week']}")
        print(f"  • Workouts: {len(result['workouts'])}")
        return True
    else:
        print(f"  ❌ Error: {response.text}")
        return False

def test_food_search():
    """Test food search"""
    response = requests.get(f"{BASE_URL}/foods/search?query=chicken&limit=5")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nFood Search:")
        print(f"  • Results: {len(result['results'])}")
        for food in result['results'][:3]:
            print(f"    - {food['name']}: {food['calories_per_100g']} kcal/100g")
        return True
    else:
        print(f"  ❌ Error: {response.text}")
        return False

def test_exercise_search():
    """Test exercise search"""
    response = requests.get(f"{BASE_URL}/exercises/search?muscle=chest&level=intermediate")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nExercise Search:")
        print(f"  • Results: {len(result['results'])}")
        for exercise in result['results'][:3]:
            print(f"    - {exercise['name']} ({exercise['level']})")
        return True
    else:
        print(f"  ❌ Error: {response.text}")
        return False

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("🧪 API Testing Suite")
    print("="*60)
    
    # Test health
    print("\n1. Testing Health Endpoint...")
    health_ok = test_health()
    
    if not health_ok:
        print("❌ Health check failed. Make sure the server is running.")
        print("   Run: uvicorn api:app --reload")
        return
    
    # Run tests
    tests = [
        ("Plan Generation", test_generate_plan),
        ("Nutrition Calculation", test_nutrition_calculation),
        ("Workout Generation", test_workout_generation),
        ("Food Search", test_food_search),
        ("Exercise Search", test_exercise_search)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n2. Testing {name}...")
        result = test_func()
        results.append((name, result))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  • {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check the output above.")

if __name__ == "__main__":
    run_all_tests()
