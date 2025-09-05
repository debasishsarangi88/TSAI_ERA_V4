from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import json
import os
import time
from datetime import datetime
import logging

# Computer Vision imports
try:
    from ultralytics import YOLO
    import torch
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("YOLO not available, falling back to deterministic analysis")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Create upload directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Enhanced Food database
FOOD_DATABASE = {
    "pizza": {
        "ingredients": ["flour", "tomato sauce", "mozzarella cheese", "basil", "olive oil", "salt", "yeast"],
        "nutrition": {"calories": 266, "protein": 11, "carbs": 33, "fat": 10, "fiber": 2},
        "allergens": ["gluten", "dairy"],
        "health_score": 6
    },
    "salad": {
        "ingredients": ["lettuce", "tomato", "cucumber", "onion", "olive oil", "vinegar", "salt", "pepper"],
        "nutrition": {"calories": 120, "protein": 3, "carbs": 8, "fat": 9, "fiber": 4},
        "allergens": [],
        "health_score": 9
    },
    "pasta": {
        "ingredients": ["pasta", "olive oil", "garlic", "parmesan cheese", "black pepper", "salt", "basil"],
        "nutrition": {"calories": 400, "protein": 15, "carbs": 60, "fat": 12, "fiber": 3},
        "allergens": ["gluten", "dairy"],
        "health_score": 7
    },
    "burger": {
        "ingredients": ["ground beef", "burger bun", "lettuce", "tomato", "onion", "cheese", "pickles", "ketchup"],
        "nutrition": {"calories": 540, "protein": 25, "carbs": 40, "fat": 31, "fiber": 3},
        "allergens": ["gluten", "dairy"],
        "health_score": 4
    },
    "sandwich": {
        "ingredients": ["bread", "turkey", "cheese", "lettuce", "tomato", "mayonnaise", "mustard"],
        "nutrition": {"calories": 320, "protein": 18, "carbs": 28, "fat": 15, "fiber": 2},
        "allergens": ["gluten", "dairy", "eggs"],
        "health_score": 6
    },
    "hot dog": {
        "ingredients": ["hot dog bun", "sausage", "mustard", "ketchup", "onions", "relish"],
        "nutrition": {"calories": 290, "protein": 11, "carbs": 25, "fat": 17, "fiber": 1},
        "allergens": ["gluten"],
        "health_score": 3
    },
    "cake": {
        "ingredients": ["flour", "sugar", "eggs", "butter", "baking powder", "vanilla", "frosting"],
        "nutrition": {"calories": 350, "protein": 4, "carbs": 55, "fat": 14, "fiber": 1},
        "allergens": ["gluten", "dairy", "eggs"],
        "health_score": 2
    },
    "dessert": {
        "ingredients": ["sugar", "milk", "cream", "flour", "eggs", "vanilla", "cardamom", "rose water"],
        "nutrition": {"calories": 280, "protein": 6, "carbs": 45, "fat": 8, "fiber": 1},
        "allergens": ["dairy", "eggs", "gluten"],
        "health_score": 3
    },
    "sweet": {
        "ingredients": ["sugar", "milk", "cream", "flour", "eggs", "vanilla", "cardamom", "rose water"],
        "nutrition": {"calories": 250, "protein": 5, "carbs": 42, "fat": 7, "fiber": 1},
        "allergens": ["dairy", "eggs", "gluten"],
        "health_score": 3
    },
    "banana": {
        "ingredients": ["banana"],
        "nutrition": {"calories": 105, "protein": 1, "carbs": 27, "fat": 0, "fiber": 3},
        "allergens": [],
        "health_score": 9
    },
    "apple": {
        "ingredients": ["apple"],
        "nutrition": {"calories": 95, "protein": 0, "carbs": 25, "fat": 0, "fiber": 4},
        "allergens": [],
        "health_score": 10
    },
    "orange": {
        "ingredients": ["orange"],
        "nutrition": {"calories": 62, "protein": 1, "carbs": 15, "fat": 0, "fiber": 3},
        "allergens": [],
        "health_score": 10
    }
}

# YOLO food class mapping (COCO dataset classes that relate to food)
YOLO_FOOD_CLASSES = {
    47: "apple",
    48: "sandwich", 
    49: "orange",
    50: "broccoli",
    51: "carrot",
    52: "hot dog",
    53: "pizza",
    54: "donut",
    55: "cake"
}

# Initialize YOLO model (if available)
yolo_model = None
if YOLO_AVAILABLE:
    try:
        # Load YOLOv8 nano model (fastest, good for demo)
        yolo_model = YOLO('yolov8n.pt')
        logger.info("YOLOv8 model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load YOLO model: {e}")
        yolo_model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_image_colors(image):
    """Analyze image colors to help with food classification - FIXED VERSION"""
    # Convert to HSV for better color analysis
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define color ranges for different foods - FIXED OVERLAPPING RANGES
    color_ranges = {
        'red': [(0, 30, 30), (10, 255, 255)],      # Pizza sauce, tomatoes
        'green': [(35, 30, 30), (85, 255, 255)],   # Vegetables, salad
        'yellow': [(20, 30, 30), (35, 255, 255)],  # Bananas (pure yellow, no orange overlap)
        'orange': [(10, 30, 30), (20, 255, 255)],  # Oranges (pure orange, no yellow overlap)
        'white': [(0, 0, 200), (180, 30, 255)],    # Desserts, cream, milk
        'pink': [(160, 30, 30), (180, 255, 255)],  # Pink desserts, flowers
    }
    
    color_percentages = {}
    total_pixels = image.shape[0] * image.shape[1]
    
    for color_name, (lower, upper) in color_ranges.items():
        lower = np.array(lower)
        upper = np.array(upper)
        mask = cv2.inRange(hsv, lower, upper)
        color_pixels = cv2.countNonZero(mask)
        color_percentages[color_name] = (color_pixels / total_pixels) * 100
    
    return color_percentages

def detect_with_yolo(image_path):
    """Use YOLO for object detection - FIXED VERSION"""
    if not yolo_model:
        return []
    
    try:
        # Run inference
        results = yolo_model(image_path)
        
        detected_objects = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    
                    # Only consider food-related classes with high confidence
                    if class_id in YOLO_FOOD_CLASSES and confidence > 0.5:  # Increased threshold
                        detected_objects.append({
                            'class_id': class_id,
                            'class_name': YOLO_FOOD_CLASSES.get(class_id, 'unknown'),
                            'confidence': confidence,
                            'bbox': box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                        })
        
        return detected_objects
    except Exception as e:
        logger.error(f"YOLO detection failed: {e}")
        return []

def classify_food_by_features(image, color_analysis):
    """Classify food based on visual features - DETERMINISTIC VERSION"""
    height, width = image.shape[:2]
    
    # Analyze image features
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Edge detection for texture analysis
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / (height * width)
    
    # Brightness analysis
    brightness = np.mean(gray)
    
    # DETERMINISTIC CLASSIFICATION LOGIC - NO RANDOM ELEMENTS
    logger.info(f"Color analysis: {color_analysis}")
    logger.info(f"Edge density: {edge_density:.4f}, Brightness: {brightness:.1f}")
    
    # Priority-based classification (most specific to least specific)
    
    # 1. Banana detection (yellow, low edge density, high brightness) - PRIORITY OVER ORANGE
    if color_analysis['yellow'] > 25 and edge_density < 0.05 and brightness > 120 and color_analysis['orange'] < 10:
        logger.info("Classified as BANANA based on yellow color, smooth texture, and low orange")
        return 'banana'
    
    # 2. Orange detection (very specific color, no yellow overlap)
    if color_analysis['orange'] > 15 and color_analysis['red'] < 5 and color_analysis['yellow'] < 10:
        logger.info("Classified as ORANGE based on orange color dominance and no yellow")
        return 'orange'
    
    # 3. Apple detection (red with some green)
    if color_analysis['red'] > 20 and color_analysis['green'] > 5 and color_analysis['green'] < 20:
        logger.info("Classified as APPLE based on red-green combination")
        return 'apple'
    
    # 4. DESSERT DETECTION (white/cream dominant, high brightness, low texture) - MORE SENSITIVE
    if color_analysis['white'] > 20 and brightness > 130 and edge_density < 0.1:
        logger.info("Classified as DESSERT based on white color, high brightness, and smooth texture")
        return 'dessert'
    
    # 5. SWEET DETECTION (white/cream with pink accents) - MORE SENSITIVE
    if color_analysis['white'] > 12 and color_analysis['pink'] > 3 and brightness > 120:
        logger.info("Classified as SWEET based on white-pink combination")
        return 'sweet'
    
    # 6. DESSERT DETECTION (high brightness, low texture, minimal colors) - FALLBACK
    if brightness > 150 and edge_density < 0.08 and (color_analysis['red'] < 5 and color_analysis['green'] < 5 and color_analysis['yellow'] < 5):
        logger.info("Classified as DESSERT based on high brightness, low texture, and minimal colors")
        return 'dessert'
    
    # 7. Pizza detection (red + yellow combination, circular shape)
    if color_analysis['red'] > 10 and color_analysis['yellow'] > 8:
        logger.info("Classified as PIZZA based on red-yellow combination")
        return 'pizza'
    
    # 8. Salad detection (green dominant)
    if color_analysis['green'] > 25:
        logger.info("Classified as SALAD based on green color dominance")
        return 'salad'
    
    # 9. Pasta detection (yellow/beige, moderate texture) - PRIORITY OVER HOT DOG
    if color_analysis['yellow'] > 20 and color_analysis['yellow'] < 50:
        logger.info("Classified as PASTA based on yellow color range")
        return 'pasta'
    
    # 10. Cake detection (high brightness, low edge density)
    if brightness > 150 and edge_density < 0.03:
        logger.info("Classified as CAKE based on high brightness and smooth texture")
        return 'cake'
    
    # 11. Burger detection (multiple colors, high texture)
    if edge_density > 0.15 and (color_analysis['red'] > 5 or color_analysis['yellow'] > 5):
        logger.info("Classified as BURGER based on high texture and mixed colors")
        return 'burger'
    
    # 12. Sandwich detection (moderate colors, moderate texture)
    if edge_density > 0.08 and edge_density < 0.15 and brightness > 100:
        logger.info("Classified as SANDWICH based on moderate texture and brightness")
        return 'sandwich'
    
    # 13. Hot dog detection (yellow dominant, low texture)
    if color_analysis['yellow'] > 15 and edge_density < 0.08:
        logger.info("Classified as HOT DOG based on yellow color and low texture")
        return 'hot dog'
    
    # IMPROVED FALLBACK LOGIC - NO MORE DEFAULTING TO PIZZA
    dominant_color = max(color_analysis.items(), key=lambda x: x[1])
    logger.info(f"No specific match found, using dominant color: {dominant_color}")
    
    # More intelligent fallback based on dominant color and features
    if dominant_color[0] == 'white' and dominant_color[1] > 12:
        logger.info("Fallback: Classified as DESSERT based on white dominance")
        return 'dessert'
    elif dominant_color[0] == 'red' and dominant_color[1] > 10:
        logger.info("Fallback: Classified as PIZZA based on red dominance")
        return 'pizza'
    elif dominant_color[0] == 'green' and dominant_color[1] > 10:
        logger.info("Fallback: Classified as SALAD based on green dominance")
        return 'salad'
    elif dominant_color[0] == 'yellow' and dominant_color[1] > 10:
        logger.info("Fallback: Classified as PASTA based on yellow dominance")
        return 'pasta'
    elif dominant_color[0] == 'orange' and dominant_color[1] > 10:
        logger.info("Fallback: Classified as ORANGE based on orange dominance")
        return 'orange'
    elif dominant_color[0] == 'pink' and dominant_color[1] > 3:
        logger.info("Fallback: Classified as SWEET based on pink dominance")
        return 'sweet'
    else:
        # Ultimate fallback - choose based on brightness and texture
        if brightness > 130 and edge_density < 0.1:
            logger.info("Ultimate fallback: Classified as DESSERT based on high brightness and low texture")
            return 'dessert'
        elif brightness > 100 and edge_density > 0.1:
            logger.info("Ultimate fallback: Classified as SANDWICH based on moderate brightness and texture")
            return 'sandwich'
        else:
            logger.info("Ultimate fallback: Classified as PASTA based on default characteristics")
            return 'pasta'

def analyze_image_with_ai(image_path):
    """Enhanced AI analysis with real computer vision - FIXED VERSION"""
    try:
        start_time = time.time()
        
        # Load and analyze the image
        image = cv2.imread(image_path)
        if image is None:
            return {
                "success": False,
                "error": "Could not load image",
                "foods": [],
                "total_foods": 0
            }
        
        detected_foods = []
        
        # Method 1: Try YOLO detection first
        yolo_detections = detect_with_yolo(image_path)
        
        if yolo_detections:
            logger.info(f"YOLO detected {len(yolo_detections)} objects")
            for detection in yolo_detections:
                food_name = detection['class_name']
                confidence = detection['confidence']
                
                # Map YOLO class to our food database
                if food_name in FOOD_DATABASE:
                    detected_foods.append({
                        "name": food_name.title(),
                        "confidence": confidence,
                        "ingredients": FOOD_DATABASE[food_name]["ingredients"],
                        "nutrition": FOOD_DATABASE[food_name]["nutrition"],
                        "allergens": FOOD_DATABASE[food_name]["allergens"],
                        "health_score": FOOD_DATABASE[food_name]["health_score"],
                        "detection_method": "YOLO"
                    })
        
        # Method 2: Use deterministic color/feature analysis if YOLO didn't find food
        if not detected_foods:
            logger.info("No YOLO detections, using deterministic color/feature analysis")
            color_analysis = analyze_image_colors(image)
            predicted_food = classify_food_by_features(image, color_analysis)
            
            # Calculate confidence based on how well the features match
            confidence = calculate_confidence(predicted_food, color_analysis, image)
            
            detected_foods.append({
                "name": predicted_food.replace('_', ' ').title(),
                "confidence": confidence,
                "ingredients": FOOD_DATABASE[predicted_food]["ingredients"],
                "nutrition": FOOD_DATABASE[predicted_food]["nutrition"],
                "allergens": FOOD_DATABASE[predicted_food]["allergens"],
                "health_score": FOOD_DATABASE[predicted_food]["health_score"],
                "detection_method": "Deterministic CV Analysis",
                "color_analysis": color_analysis
            })
        
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "foods": detected_foods,
            "total_foods": len(detected_foods),
            "processing_time": round(processing_time, 2),
            "ai_model": "YOLOv8 + Enhanced CV Pipeline v3.0",
            "yolo_available": YOLO_AVAILABLE,
            "image_dimensions": image.shape[:2]
        }
        
    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "foods": [],
            "total_foods": 0
        }

def calculate_confidence(predicted_food, color_analysis, image):
    """Calculate confidence based on feature matching - DETERMINISTIC"""
    base_confidence = 0.7  # Base confidence for CV analysis
    
    # Analyze how well the prediction matches the image features
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / (image.shape[0] * image.shape[1])
    brightness = np.mean(gray)
    
    confidence_boost = 0.0
    
    # Boost confidence based on how well features match expected patterns
    if predicted_food == 'pizza' and color_analysis['red'] > 10 and color_analysis['yellow'] > 8:
        confidence_boost += 0.2
    elif predicted_food == 'salad' and color_analysis['green'] > 25:
        confidence_boost += 0.2
    elif predicted_food == 'pasta' and color_analysis['yellow'] > 20:
        confidence_boost += 0.2
    elif predicted_food == 'orange' and color_analysis['orange'] > 15:
        confidence_boost += 0.2
    elif predicted_food == 'banana' and color_analysis['yellow'] > 25 and edge_density < 0.05:
        confidence_boost += 0.2
    elif predicted_food == 'dessert' and color_analysis['white'] > 20 and brightness > 130:
        confidence_boost += 0.2
    elif predicted_food == 'sweet' and color_analysis['white'] > 12 and color_analysis['pink'] > 3:
        confidence_boost += 0.2
    
    # Boost for high feature match
    if edge_density > 0.1:  # Complex texture
        confidence_boost += 0.1
    
    final_confidence = min(0.95, base_confidence + confidence_boost)
    return round(final_confidence, 3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "3.3.0",
        "yolo_available": YOLO_AVAILABLE,
        "cv_features": {
            "yolo_detection": YOLO_AVAILABLE,
            "deterministic_analysis": True,
            "color_analysis": True,
            "feature_extraction": True,
            "multi_food_detection": True,
            "no_randomness": True,
            "dessert_detection": True,
            "enhanced_fallback": True
        }
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_food():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "File type not allowed"}), 400
        
        # Save file
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Analyze image with enhanced AI
        result = analyze_image_with_ai(file_path)
        result["filename"] = filename
        result["timestamp"] = datetime.now().isoformat()
        
        # Clean up
        try:
            os.remove(file_path)
        except:
            pass
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/foods')
def get_food_database():
    return jsonify({
        "success": True,
        "foods": FOOD_DATABASE,
        "total_foods": len(FOOD_DATABASE)
    })

@app.route('/api/stats')
def get_stats():
    return jsonify({
        "success": True,
        "total_food_types": len(FOOD_DATABASE),
        "yolo_available": YOLO_AVAILABLE,
        "supported_formats": list(ALLOWED_EXTENSIONS),
        "max_file_size": MAX_FILE_SIZE,
        "cv_methods": [
            "YOLOv8 Object Detection",
            "Enhanced Color Analysis (with white/pink)",
            "Feature Extraction",
            "Edge Detection",
            "Brightness Analysis",
            "Dessert Detection",
            "No Random Elements",
            "Improved Fallback Logic"
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
