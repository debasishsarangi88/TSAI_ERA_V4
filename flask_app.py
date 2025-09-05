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

# Food database
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
    }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_image_with_ai(image_path):
    """Mock AI analysis - replace with actual AI model"""
    try:
        time.sleep(2)  # Simulate processing
        
        # Load and analyze the image
        image = cv2.imread(image_path)
        if image is None:
            return {
                "success": False,
                "error": "Could not load image",
                "foods": [],
                "total_foods": 0
            }
        
        # Get image dimensions for analysis
        height, width = image.shape[:2]
        
        detected_foods = []
        
        # Simulate AI analysis based on image characteristics
        # For demo purposes, we'll detect different foods based on image size and random factors
        rand_factor = np.random.random()
        
        # Always detect at least one food item for demo purposes
        if rand_factor < 0.3:
            # Detect pizza
            detected_foods.append({
                "name": "Pizza Margherita",
                "confidence": 0.92 + np.random.random() * 0.08,
                "ingredients": FOOD_DATABASE["pizza"]["ingredients"],
                "nutrition": FOOD_DATABASE["pizza"]["nutrition"],
                "allergens": FOOD_DATABASE["pizza"]["allergens"],
                "health_score": FOOD_DATABASE["pizza"]["health_score"]
            })
        elif rand_factor < 0.6:
            # Detect salad
            detected_foods.append({
                "name": "Fresh Garden Salad",
                "confidence": 0.88 + np.random.random() * 0.12,
                "ingredients": FOOD_DATABASE["salad"]["ingredients"],
                "nutrition": FOOD_DATABASE["salad"]["nutrition"],
                "allergens": FOOD_DATABASE["salad"]["allergens"],
                "health_score": FOOD_DATABASE["salad"]["health_score"]
            })
        else:
            # Detect pasta
            detected_foods.append({
                "name": "Spaghetti Aglio e Olio",
                "confidence": 0.90 + np.random.random() * 0.10,
                "ingredients": FOOD_DATABASE["pasta"]["ingredients"],
                "nutrition": FOOD_DATABASE["pasta"]["nutrition"],
                "allergens": FOOD_DATABASE["pasta"]["allergens"],
                "health_score": FOOD_DATABASE["pasta"]["health_score"]
            })
        
        # Sometimes detect multiple foods
        if np.random.random() < 0.3 and len(detected_foods) > 0:
            # Add a second food item
            additional_foods = [
                {
                    "name": "French Fries",
                    "confidence": 0.85 + np.random.random() * 0.15,
                    "ingredients": ["potatoes", "vegetable oil", "salt", "black pepper"],
                    "nutrition": {"calories": 365, "protein": 4, "carbs": 63, "fat": 11, "fiber": 6},
                    "allergens": [],
                    "health_score": 4
                },
                {
                    "name": "Chicken Nuggets",
                    "confidence": 0.87 + np.random.random() * 0.13,
                    "ingredients": ["chicken breast", "flour", "eggs", "breadcrumbs", "salt", "pepper", "oil"],
                    "nutrition": {"calories": 296, "protein": 18, "carbs": 15, "fat": 18, "fiber": 1},
                    "allergens": ["gluten", "eggs"],
                    "health_score": 5
                }
            ]
            detected_foods.append(np.random.choice(additional_foods))
        
        return {
            "success": True,
            "foods": detected_foods,
            "total_foods": len(detected_foods),
            "processing_time": 2.1 + np.random.random() * 0.5,
            "ai_model": "FoodVision Pro v2.1"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "foods": [],
            "total_foods": 0
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.1.0"
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
        
        # Analyze image
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
