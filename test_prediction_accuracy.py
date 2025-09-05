#!/usr/bin/env python3
"""
Test script to verify actual prediction accuracy and identify random behavior
"""

import cv2
import numpy as np
import os
import sys
import time
from flask_app_cv import analyze_image_with_ai, analyze_image_colors, classify_food_by_features

def create_test_images():
    """Create specific test images for different food types"""
    print("🖼️  Creating test images for accuracy testing...")
    
    test_images = {}
    
    # 1. Pizza-like image (red and yellow)
    pizza_img = np.zeros((300, 300, 3), dtype=np.uint8)
    # Red base (tomato sauce)
    cv2.circle(pizza_img, (150, 150), 100, (0, 0, 255), -1)
    # Yellow cheese
    cv2.circle(pizza_img, (150, 150), 80, (0, 255, 255), -1)
    # White mozzarella
    cv2.circle(pizza_img, (150, 150), 60, (255, 255, 255), -1)
    cv2.imwrite('test_pizza.jpg', pizza_img)
    test_images['pizza'] = 'test_pizza.jpg'
    
    # 2. Salad-like image (green)
    salad_img = np.zeros((300, 300, 3), dtype=np.uint8)
    # Green lettuce
    cv2.rectangle(salad_img, (50, 50), (250, 250), (0, 255, 0), -1)
    # Red tomatoes
    cv2.circle(salad_img, (100, 100), 20, (0, 0, 255), -1)
    cv2.circle(salad_img, (200, 150), 20, (0, 0, 255), -1)
    # White dressing
    cv2.circle(salad_img, (150, 200), 15, (255, 255, 255), -1)
    cv2.imwrite('test_salad.jpg', salad_img)
    test_images['salad'] = 'test_salad.jpg'
    
    # 3. Pasta-like image (yellow/beige)
    pasta_img = np.zeros((300, 300, 3), dtype=np.uint8)
    # Yellow pasta
    cv2.rectangle(pasta_img, (50, 50), (250, 250), (0, 255, 255), -1)
    # White sauce
    cv2.rectangle(pasta_img, (100, 100), (200, 200), (255, 255, 255), -1)
    cv2.imwrite('test_pasta.jpg', pasta_img)
    test_images['pasta'] = 'test_pasta.jpg'
    
    # 4. Orange-like image (orange)
    orange_img = np.zeros((300, 300, 3), dtype=np.uint8)
    # Orange color
    cv2.circle(orange_img, (150, 150), 80, (0, 165, 255), -1)
    cv2.imwrite('test_orange.jpg', orange_img)
    test_images['orange'] = 'test_orange.jpg'
    
    # 5. Banana-like image (yellow)
    banana_img = np.zeros((300, 300, 3), dtype=np.uint8)
    # Yellow banana shape
    cv2.ellipse(banana_img, (150, 150), (60, 100), 0, 0, 360, (0, 255, 255), -1)
    cv2.imwrite('test_banana.jpg', banana_img)
    test_images['banana'] = 'test_banana.jpg'
    
    return test_images

def test_color_analysis():
    """Test color analysis function"""
    print("\n🎨 Testing Color Analysis...")
    
    test_images = create_test_images()
    
    for food_type, image_path in test_images.items():
        print(f"\n--- Testing {food_type.upper()} ---")
        
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Could not load {image_path}")
            continue
        
        # Test color analysis
        color_analysis = analyze_image_colors(image)
        print(f"Color analysis: {color_analysis}")
        
        # Test feature classification
        predicted = classify_food_by_features(image, color_analysis)
        print(f"Predicted food: {predicted}")
        print(f"Expected: {food_type}")
        print(f"✅ Correct" if predicted == food_type else f"❌ Wrong prediction")

def test_multiple_predictions():
    """Test the same image multiple times to check for randomness"""
    print("\n🎲 Testing for Randomness (Same Image, Multiple Predictions)...")
    
    # Use pizza image for testing
    image_path = 'test_pizza.jpg'
    if not os.path.exists(image_path):
        create_test_images()
    
    predictions = []
    print(f"Testing image: {image_path}")
    
    for i in range(10):
        print(f"\n--- Prediction {i+1}/10 ---")
        result = analyze_image_with_ai(image_path)
        
        if result['success'] and result['foods']:
            food_name = result['foods'][0]['name'].lower()
            confidence = result['foods'][0]['confidence']
            method = result['foods'][0].get('detection_method', 'Unknown')
            predictions.append({
                'food': food_name,
                'confidence': confidence,
                'method': method
            })
            print(f"Predicted: {food_name} (confidence: {confidence:.3f}, method: {method})")
        else:
            print(f"❌ No prediction: {result.get('error', 'Unknown error')}")
    
    # Analyze results
    print(f"\n📊 Randomness Analysis:")
    unique_predictions = set(p['food'] for p in predictions)
    print(f"Unique predictions: {len(unique_predictions)}")
    print(f"Predictions: {unique_predictions}")
    
    if len(unique_predictions) > 1:
        print("❌ RANDOM BEHAVIOR DETECTED - Same image gives different predictions!")
        for pred in unique_predictions:
            count = sum(1 for p in predictions if p['food'] == pred)
            print(f"  {pred}: {count}/10 times")
    else:
        print("✅ Consistent predictions - No randomness detected")

def test_yolo_detection():
    """Test YOLO detection specifically"""
    print("\n🎯 Testing YOLO Detection...")
    
    try:
        from ultralytics import YOLO
        from flask_app_cv import detect_with_yolo
        
        # Test with pizza image
        image_path = 'test_pizza.jpg'
        if not os.path.exists(image_path):
            create_test_images()
        
        print(f"Testing YOLO on: {image_path}")
        detections = detect_with_yolo(image_path)
        
        print(f"YOLO detections: {len(detections)}")
        for detection in detections:
            print(f"  Class: {detection['class_name']}, Confidence: {detection['confidence']:.3f}")
        
        if not detections:
            print("⚠️  YOLO found no food objects - this is expected for synthetic images")
            print("   YOLO is trained on real photos, not synthetic test images")
        
    except ImportError:
        print("❌ YOLO not available")
    except Exception as e:
        print(f"❌ YOLO test failed: {e}")

def test_real_image_analysis():
    """Test with a more realistic synthetic image"""
    print("\n🖼️  Testing with More Realistic Image...")
    
    # Create a more realistic pizza image
    pizza_img = np.zeros((400, 400, 3), dtype=np.uint8)
    
    # Background (plate)
    cv2.circle(pizza_img, (200, 200), 180, (200, 200, 200), -1)
    
    # Pizza base (darker)
    cv2.circle(pizza_img, (200, 200), 160, (139, 69, 19), -1)
    
    # Tomato sauce (red)
    cv2.circle(pizza_img, (200, 200), 140, (0, 0, 200), -1)
    
    # Cheese (yellow)
    cv2.circle(pizza_img, (200, 200), 120, (0, 200, 200), -1)
    
    # Toppings (green basil)
    cv2.circle(pizza_img, (150, 150), 10, (0, 255, 0), -1)
    cv2.circle(pizza_img, (250, 150), 10, (0, 255, 0), -1)
    cv2.circle(pizza_img, (200, 250), 10, (0, 255, 0), -1)
    
    cv2.imwrite('realistic_pizza.jpg', pizza_img)
    
    print("Created realistic pizza image")
    
    # Test multiple times
    predictions = []
    for i in range(5):
        result = analyze_image_with_ai('realistic_pizza.jpg')
        if result['success'] and result['foods']:
            food_name = result['foods'][0]['name'].lower()
            predictions.append(food_name)
            print(f"Prediction {i+1}: {food_name}")
    
    unique_predictions = set(predictions)
    print(f"\nUnique predictions: {unique_predictions}")
    if len(unique_predictions) > 1:
        print("❌ Still random behavior detected!")
    else:
        print("✅ Consistent predictions")

def main():
    """Run all accuracy tests"""
    print("🔍 Food Prediction Accuracy Test Suite")
    print("=" * 60)
    
    # Test 1: Color analysis
    test_color_analysis()
    
    # Test 2: Randomness check
    test_multiple_predictions()
    
    # Test 3: YOLO detection
    test_yolo_detection()
    
    # Test 4: Realistic image
    test_real_image_analysis()
    
    # Cleanup
    print("\n🧹 Cleaning up test images...")
    test_files = ['test_pizza.jpg', 'test_salad.jpg', 'test_pasta.jpg', 
                  'test_orange.jpg', 'test_banana.jpg', 'realistic_pizza.jpg']
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n✅ Accuracy testing complete!")

if __name__ == "__main__":
    main()
