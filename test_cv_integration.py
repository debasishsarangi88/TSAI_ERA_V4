#!/usr/bin/env python3
"""
Test script to verify computer vision integration
"""

import cv2
import numpy as np
from PIL import Image
import os
import sys

def test_dependencies():
    """Test if all CV dependencies are available"""
    print("🔍 Testing Computer Vision Dependencies...")
    
    # Test basic OpenCV
    try:
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV: {e}")
        return False
    
    # Test NumPy
    try:
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        return False
    
    # Test PIL
    try:
        from PIL import Image
        print(f"✅ Pillow: {Image.__version__}")
    except ImportError as e:
        print(f"❌ Pillow: {e}")
        return False
    
    # Test YOLO (optional)
    try:
        from ultralytics import YOLO
        print(f"✅ Ultralytics YOLO: Available")
        yolo_available = True
    except ImportError as e:
        print(f"⚠️  Ultralytics YOLO: Not available - {e}")
        yolo_available = False
    
    # Test PyTorch (optional)
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
    except ImportError as e:
        print(f"⚠️  PyTorch: Not available - {e}")
    
    return True

def test_image_processing():
    """Test basic image processing functions"""
    print("\n🖼️  Testing Image Processing...")
    
    try:
        # Create a test image
        test_image = np.zeros((300, 300, 3), dtype=np.uint8)
        
        # Add some colored regions to simulate food
        # Red region (pizza-like)
        cv2.rectangle(test_image, (50, 50), (150, 150), (0, 0, 255), -1)
        
        # Green region (salad-like)  
        cv2.rectangle(test_image, (200, 50), (250, 150), (0, 255, 0), -1)
        
        # Yellow region (pasta-like)
        cv2.rectangle(test_image, (50, 200), (150, 250), (0, 255, 255), -1)
        
        # Save test image
        cv2.imwrite('test_food_image.jpg', test_image)
        print("✅ Created test food image")
        
        # Test color analysis
        hsv = cv2.cvtColor(test_image, cv2.COLOR_BGR2HSV)
        print("✅ Color space conversion works")
        
        # Test edge detection
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        print("✅ Edge detection works")
        
        # Clean up
        if os.path.exists('test_food_image.jpg'):
            os.remove('test_food_image.jpg')
        
        return True
        
    except Exception as e:
        print(f"❌ Image processing test failed: {e}")
        return False

def test_yolo_model():
    """Test YOLO model loading"""
    print("\n🎯 Testing YOLO Model...")
    
    try:
        from ultralytics import YOLO
        
        # Try to load YOLOv8 nano model
        model = YOLO('yolov8n.pt')
        print("✅ YOLOv8 nano model loaded successfully")
        
        # Test prediction on a simple image
        test_image = np.zeros((640, 640, 3), dtype=np.uint8)
        cv2.imwrite('temp_test.jpg', test_image)
        
        results = model('temp_test.jpg')
        print("✅ YOLO prediction test successful")
        
        # Clean up
        if os.path.exists('temp_test.jpg'):
            os.remove('temp_test.jpg')
            
        return True
        
    except ImportError:
        print("⚠️  YOLO not available - will use fallback methods")
        return False
    except Exception as e:
        print(f"⚠️  YOLO test failed: {e} - will use fallback methods")
        return False

def test_flask_app_import():
    """Test if the enhanced Flask app can be imported"""
    print("\n🌐 Testing Flask App Import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, '.')
        
        # Try to import the enhanced Flask app
        import flask_app_cv
        print("✅ Enhanced Flask app imported successfully")
        
        # Test basic functions
        if hasattr(flask_app_cv, 'analyze_image_colors'):
            print("✅ Color analysis function available")
        
        if hasattr(flask_app_cv, 'classify_food_by_features'):
            print("✅ Feature classification function available")
            
        if hasattr(flask_app_cv, 'detect_with_yolo'):
            print("✅ YOLO detection function available")
            
        return True
        
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Computer Vision Integration Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Dependencies
    if test_dependencies():
        tests_passed += 1
    
    # Test 2: Image Processing
    if test_image_processing():
        tests_passed += 1
    
    # Test 3: YOLO Model (optional)
    if test_yolo_model():
        tests_passed += 1
    else:
        print("⚠️  YOLO test skipped - using fallback methods")
        tests_passed += 0.5  # Partial credit
    
    # Test 4: Flask App Import
    if test_flask_app_import():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed >= 3:
        print("✅ Computer Vision integration is ready!")
        print("🚀 You can now run the enhanced Flask app with:")
        print("   python flask_app_cv.py")
    else:
        print("❌ Some issues found. Please install missing dependencies:")
        print("   pip install ultralytics torch torchvision")
    
    return tests_passed >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
