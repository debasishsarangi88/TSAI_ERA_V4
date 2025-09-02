#!/usr/bin/env python3
"""
Demo script for AI Food Ingredient Scanner
This script demonstrates the core functionality without the full Streamlit interface
"""

import time
from PIL import Image
import numpy as np
from ai_food_scanner import analyze_image_with_ai, get_health_recommendations, create_nutrition_chart

def create_demo_image():
    """Create a simple demo image for testing"""
    # Create a 400x300 RGB image with some colors
    img_array = np.zeros((300, 400, 3), dtype=np.uint8)
    
    # Add some colored rectangles to simulate food items
    # Pizza area (red)
    img_array[50:150, 50:200] = [255, 100, 100]
    # Salad area (green)
    img_array[50:150, 250:350] = [100, 255, 100]
    # Pasta area (yellow)
    img_array[200:280, 100:300] = [255, 255, 100]
    
    # Convert to PIL Image
    img = Image.fromarray(img_array)
    return img

def main():
    print("🍽️ AI Food Ingredient Scanner Demo")
    print("=" * 50)
    
    # Create demo image
    print("📸 Creating demo image...")
    demo_image = create_demo_image()
    print(f"✅ Image created: {demo_image.size[0]}x{demo_image.size[1]} pixels")
    
    # Analyze image
    print("\n🤖 Analyzing image with AI...")
    start_time = time.time()
    
    results = analyze_image_with_ai(demo_image)
    
    end_time = time.time()
    actual_time = end_time - start_time
    
    print(f"✅ Analysis completed in {actual_time:.2f}s")
    print(f"📊 AI Model: {results['ai_model']}")
    print(f"🍕 Foods detected: {results['total_foods']}")
    
    # Display results
    print("\n🎯 Detection Results:")
    print("-" * 30)
    
    for i, food in enumerate(results['foods'], 1):
        print(f"\n{i}. {food['name']}")
        print(f"   Confidence: {food['confidence']:.1%}")
        print(f"   Health Score: {food['health_score']}/10")
        print(f"   Ingredients: {', '.join(food['ingredients'])}")
        print(f"   Calories: {food['nutrition']['calories']}")
        print(f"   Protein: {food['nutrition']['protein']}g")
        print(f"   Carbs: {food['nutrition']['carbs']}g")
        print(f"   Fat: {food['nutrition']['fat']}g")
        
        if food['allergens']:
            print(f"   ⚠️  Allergens: {', '.join(food['allergens'])}")
    
    # Health recommendations
    if results['foods']:
        print("\n💡 Health Recommendations:")
        print("-" * 30)
        recommendations = get_health_recommendations(results['foods'])
        for rec in recommendations:
            print(f"   {rec}")
    
    # Nutrition summary
    if len(results['foods']) > 1:
        print("\n📊 Nutrition Summary:")
        print("-" * 30)
        total_calories = sum(food['nutrition']['calories'] for food in results['foods'])
        total_protein = sum(food['nutrition']['protein'] for food in results['foods'])
        total_carbs = sum(food['nutrition']['carbs'] for food in results['foods'])
        total_fat = sum(food['nutrition']['fat'] for food in results['foods'])
        
        print(f"   Total Calories: {total_calories}")
        print(f"   Total Protein: {total_protein}g")
        print(f"   Total Carbs: {total_carbs}g")
        print(f"   Total Fat: {total_fat}g")
    
    print("\n🎉 Demo completed successfully!")
    print("🚀 Run 'streamlit run ai_food_scanner.py' to launch the full web app!")

if __name__ == "__main__":
    main()
