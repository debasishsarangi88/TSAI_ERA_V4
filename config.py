import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_CLOUD_VISION_API_KEY = os.getenv('GOOGLE_CLOUD_VISION_API_KEY', '')
AZURE_COMPUTER_VISION_KEY = os.getenv('AZURE_COMPUTER_VISION_KEY', '')
AZURE_COMPUTER_VISION_ENDPOINT = os.getenv('AZURE_COMPUTER_VISION_ENDPOINT', '')

# App Configuration
APP_NAME = "AI Food Ingredient Scanner Pro"
APP_VERSION = "2.1.0"
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

# Food Recognition Settings
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.7'))
MAX_FOOD_ITEMS = int(os.getenv('MAX_FOOD_ITEMS', '10'))
PROCESSING_TIMEOUT = int(os.getenv('PROCESSING_TIMEOUT', '30'))

# Database Configuration
FOOD_DATABASE_PATH = os.getenv('FOOD_DATABASE_PATH', 'food_database.json')
NUTRITION_API_URL = os.getenv('NUTRITION_API_URL', 'https://api.edamam.com/api/nutrition-data')

# UI Configuration
THEME_COLORS = {
    'primary': '#FF6B6B',
    'secondary': '#4ECDC4',
    'accent': '#45B7D1',
    'success': '#96CEB4',
    'warning': '#FFEAA7',
    'error': '#DDA0A0'
}

# Supported image formats
SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff']

# Health analysis thresholds
HEALTH_THRESHOLDS = {
    'high_calories': 800,
    'low_protein': 20,
    'high_fat': 40,
    'low_fiber': 3
}
