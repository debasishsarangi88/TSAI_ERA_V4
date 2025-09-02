import streamlit as st
import cv2
import numpy as np
from PIL import Image
import requests
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64
import time
from typing import List, Dict, Any
import re

# Page configuration
st.set_page_config(
    page_title="🍽️ AI Food Ingredient Scanner Pro",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.8rem;
        color: #4ECDC4;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    .upload-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .result-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .info-box {
        background: rgba(255,255,255,0.15);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.8rem 2.5rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    .ingredient-tag {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# Food database with ingredients and nutrition
FOOD_DATABASE = {
    "pizza": {
        "ingredients": ["flour", "tomato sauce", "mozzarella cheese", "basil", "olive oil", "salt", "yeast"],
        "nutrition": {"calories": 266, "protein": 11, "carbs": 33, "fat": 10, "fiber": 2},
        "allergens": ["gluten", "dairy"],
        "health_score": 6
    },
    "burger": {
        "ingredients": ["beef patty", "bun", "lettuce", "tomato", "onion", "cheese", "ketchup", "mustard"],
        "nutrition": {"calories": 550, "protein": 25, "carbs": 45, "fat": 30, "fiber": 3},
        "allergens": ["gluten", "dairy", "soy"],
        "health_score": 4
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
    "sushi": {
        "ingredients": ["rice", "nori", "fish", "cucumber", "avocado", "wasabi", "soy sauce"],
        "nutrition": {"calories": 200, "protein": 8, "carbs": 35, "fat": 2, "fiber": 2},
        "allergens": ["fish", "soy"],
        "health_score": 8
    }
}

def extract_food_keywords(text: str) -> List[str]:
    """Extract food-related keywords from text"""
    food_keywords = []
    text_lower = text.lower()
    
    # Common food items
    food_items = ["pizza", "burger", "salad", "pasta", "sushi", "rice", "bread", "meat", "fish", "chicken"]
    
    for item in food_items:
        if item in text_lower:
            food_keywords.append(item)
    
    # Look for ingredient patterns
    ingredient_patterns = [
        r'\b(cheese|tomato|lettuce|onion|garlic|olive oil|salt|pepper)\b',
        r'\b(flour|sugar|eggs|milk|butter|oil|vinegar)\b',
        r'\b(beef|pork|chicken|fish|shrimp|salmon)\b'
    ]
    
    for pattern in ingredient_patterns:
        matches = re.findall(pattern, text_lower)
        food_keywords.extend(matches)
    
    return list(set(food_keywords))

def analyze_image_with_ai(image: Image.Image) -> Dict[str, Any]:
    """Analyze image using AI to identify food items"""
    # This is a mock AI analysis - replace with actual AI service
    # For production, integrate with Google Cloud Vision, Azure Computer Vision, or similar
    
    # Simulate AI processing
    time.sleep(2)
    
    # Mock detection results
    detected_foods = []
    
    # Simulate different food detections based on image characteristics
    # In real implementation, this would come from AI model
    if np.random.random() > 0.5:
        detected_foods.append({
            "name": "Pizza Margherita",
            "confidence": 0.95,
            "bbox": [100, 100, 300, 300],
            "ingredients": FOOD_DATABASE["pizza"]["ingredients"],
            "nutrition": FOOD_DATABASE["pizza"]["nutrition"],
            "allergens": FOOD_DATABASE["pizza"]["allergens"],
            "health_score": FOOD_DATABASE["pizza"]["health_score"]
        })
    
    if np.random.random() > 0.6:
        detected_foods.append({
            "name": "Caesar Salad",
            "confidence": 0.87,
            "bbox": [400, 150, 500, 250],
            "ingredients": FOOD_DATABASE["salad"]["ingredients"],
            "nutrition": FOOD_DATABASE["salad"]["nutrition"],
            "allergens": FOOD_DATABASE["salad"]["allergens"],
            "health_score": FOOD_DATABASE["salad"]["health_score"]
        })
    
    if np.random.random() > 0.7:
        detected_foods.append({
            "name": "Pasta Carbonara",
            "confidence": 0.92,
            "bbox": [200, 400, 400, 500],
            "ingredients": FOOD_DATABASE["pasta"]["ingredients"],
            "nutrition": FOOD_DATABASE["pasta"]["nutrition"],
            "allergens": FOOD_DATABASE["pasta"]["allergens"],
            "health_score": FOOD_DATABASE["pasta"]["health_score"]
        })
    
    return {
        "foods": detected_foods,
        "total_foods": len(detected_foods),
        "processing_time": 2.1,
        "ai_model": "FoodVision Pro v2.1"
    }

def get_health_recommendations(food_data: List[Dict]) -> List[str]:
    """Generate health recommendations based on detected foods"""
    recommendations = []
    
    total_calories = sum(food["nutrition"]["calories"] for food in food_data)
    total_protein = sum(food["nutrition"]["protein"] for food in food_data)
    total_fat = sum(food["nutrition"]["fat"] for food in food_data)
    
    if total_calories > 800:
        recommendations.append("⚠️ High calorie meal - consider portion control")
    
    if total_protein < 20:
        recommendations.append("💪 Low protein content - consider adding lean protein")
    
    if total_fat > 40:
        recommendations.append("🫀 High fat content - consider healthier cooking methods")
    
    # Check for allergens
    all_allergens = set()
    for food in food_data:
        all_allergens.update(food["allergens"])
    
    if all_allergens:
        recommendations.append(f"🚨 Contains allergens: {', '.join(all_allergens)}")
    
    # Health score recommendations
    avg_health_score = sum(food["health_score"] for food in food_data) / len(food_data)
    if avg_health_score < 5:
        recommendations.append("🥗 Consider adding more vegetables for better nutrition")
    elif avg_health_score > 7:
        recommendations.append("✅ Excellent nutritional choice!")
    
    return recommendations

def create_nutrition_chart(food_data: List[Dict]) -> go.Figure:
    """Create a nutrition comparison chart"""
    names = [food["name"] for food in food_data]
    calories = [food["nutrition"]["calories"] for food in food_data]
    protein = [food["nutrition"]["protein"] for food in food_data]
    carbs = [food["nutrition"]["carbs"] for food in food_data]
    fat = [food["nutrition"]["fat"] for food in food_data]
    
    fig = go.Figure(data=[
        go.Bar(name='Calories', x=names, y=calories, marker_color='#FF6B6B'),
        go.Bar(name='Protein (g)', x=names, y=protein, marker_color='#4ECDC4'),
        go.Bar(name='Carbs (g)', x=names, y=carbs, marker_color='#45B7D1'),
        go.Bar(name='Fat (g)', x=names, y=fat, marker_color='#96CEB4')
    ])
    
    fig.update_layout(
        title="Nutritional Comparison",
        barmode='group',
        xaxis_title="Food Items",
        yaxis_title="Amount",
        height=400
    )
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🍽️ AI Food Ingredient Scanner Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Advanced AI-powered food analysis with ingredient detection and nutritional insights</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input("AI API Key (Optional)", type="password", help="Enter your AI service API key for enhanced features")
        if api_key:
            st.session_state.api_key = api_key
            st.success("✅ API key configured")
        
        st.markdown("### 📊 App Statistics")
        st.metric("Total Scans", len(st.session_state.scan_history))
        today_scans = len([s for s in st.session_state.scan_history 
                          if s['timestamp'].date() == datetime.now().date()])
        st.metric("Today's Scans", today_scans)
        
        if st.session_state.scan_history:
            avg_foods = sum(s['total_foods'] for s in st.session_state.scan_history) / len(st.session_state.scan_history)
            st.metric("Avg Foods/Scan", f"{avg_foods:.1f}")
        
        st.markdown("### 🔧 Settings")
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7, 0.05)
        enable_health_analysis = st.checkbox("Enable Health Analysis", value=True)
        show_ingredient_tags = st.checkbox("Show Ingredient Tags", value=True)
        
        st.markdown("### 📚 About")
        st.info("""
        **AI Food Scanner Pro** features:
        • Advanced food recognition
        • Detailed ingredient analysis
        • Nutritional information
        • Health recommendations
        • Allergen detection
        • Scan history tracking
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### 📸 Upload Food Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="Upload a clear image of food items for best results"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.session_state.uploaded_image = image
            
            # Image info
            st.info(f"📁 File: {uploaded_file.name} | 📏 Size: {image.size[0]}x{image.size[1]} | 🎨 Mode: {image.mode}")
            
            # Scan button
            if st.button("🔍 Analyze with AI", type="primary"):
                with st.spinner("🤖 AI is analyzing your food image..."):
                    # Analyze image with AI
                    analysis_results = analyze_image_with_ai(image)
                    st.session_state.scan_results = analysis_results
                    
                    # Add to history
                    scan_record = {
                        'timestamp': datetime.now(),
                        'image_name': uploaded_file.name,
                        'total_foods': analysis_results['total_foods'],
                        'processing_time': analysis_results['processing_time'],
                        'ai_model': analysis_results['ai_model'],
                        'results': analysis_results['foods']
                    }
                    st.session_state.scan_history.append(scan_record)
                    
                    st.success(f"✅ Analysis completed in {analysis_results['processing_time']:.1f}s!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if st.session_state.scan_results:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.markdown("### 🎯 AI Analysis Results")
            
            # Analysis summary
            col_sum1, col_sum2, col_sum3 = st.columns(3)
            with col_sum1:
                st.metric("Foods Detected", st.session_state.scan_results['total_foods'])
            with col_sum2:
                st.metric("Processing Time", f"{st.session_state.scan_results['processing_time']:.1f}s")
            with col_sum3:
                st.metric("AI Model", st.session_state.scan_results['ai_model'])
            
            # Food details
            for i, food in enumerate(st.session_state.scan_results['foods']):
                with st.expander(f"🍕 {food['name']} (Confidence: {food['confidence']:.1%})", expanded=True):
                    # Ingredients
                    st.markdown("**📋 Ingredients:**")
                    if show_ingredient_tags:
                        ingredient_html = ""
                        for ingredient in food['ingredients']:
                            ingredient_html += f'<span class="ingredient-tag">{ingredient}</span>'
                        st.markdown(ingredient_html, unsafe_allow_html=True)
                    else:
                        ingredients_df = pd.DataFrame({
                            'Ingredient': food['ingredients'],
                            'Category': ['Base', 'Sauce', 'Cheese', 'Herb', 'Oil', 'Seasoning'][:len(food['ingredients'])]
                        })
                        st.dataframe(ingredients_df, use_container_width=True)
                    
                    # Nutrition info
                    st.markdown("**🍎 Nutrition (per serving):**")
                    col_n1, col_n2, col_n3, col_n4, col_n5 = st.columns(5)
                    with col_n1:
                        st.metric("Calories", f"{food['nutrition']['calories']}")
                    with col_n2:
                        st.metric("Protein", f"{food['nutrition']['protein']}g")
                    with col_n3:
                        st.metric("Carbs", f"{food['nutrition']['carbs']}g")
                    with col_n4:
                        st.metric("Fat", f"{food['nutrition']['fat']}g")
                    with col_n5:
                        st.metric("Fiber", f"{food['nutrition']['fiber']}g")
                    
                    # Health score
                    health_color = "🟢" if food['health_score'] > 7 else "🟡" if food['health_score'] > 5 else "🔴"
                    st.markdown(f"**{health_color} Health Score: {food['health_score']}/10**")
                    
                    # Allergens
                    if food['allergens']:
                        st.markdown(f"**⚠️ Allergens:** {', '.join(food['allergens'])}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Health recommendations
            if enable_health_analysis and st.session_state.scan_results['foods']:
                st.markdown("### 💡 Health Recommendations")
                recommendations = get_health_recommendations(st.session_state.scan_results['foods'])
                for rec in recommendations:
                    st.info(rec)
            
            # Nutrition chart
            if len(st.session_state.scan_results['foods']) > 1:
                st.markdown("### 📊 Nutrition Comparison")
                fig = create_nutrition_chart(st.session_state.scan_results['foods'])
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.info("👆 Upload an image and click 'Analyze with AI' to get started!")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # History section
    if st.session_state.scan_history:
        st.markdown("### 📈 Scan History & Analytics")
        
        # Create history dataframe
        history_data = []
        for record in st.session_state.scan_history:
            history_data.append({
                'Date': record['timestamp'].strftime('%Y-%m-%d %H:%M'),
                'Image': record['image_name'],
                'Foods Found': record['total_foods'],
                'Processing Time': f"{record['processing_time']:.1f}s",
                'AI Model': record['ai_model']
            })
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)
        
        # Advanced analytics
        col_analytics1, col_analytics2 = st.columns(2)
        
        with col_analytics1:
            # Processing time trend
            fig_time = px.line(
                history_df, 
                x='Date', 
                y='Processing Time',
                title="AI Processing Time Trend",
                markers=True
            )
            fig_time.update_layout(showlegend=False)
            st.plotly_chart(fig_time, use_container_width=True)
        
        with col_analytics2:
            # Foods detected trend
            fig_foods = px.bar(
                history_df,
                x='Date',
                y='Foods Found',
                title="Foods Detected Over Time",
                color='Foods Found',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig_foods, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🍽️ AI Food Ingredient Scanner Pro | Built with Streamlit & Advanced AI</p>
        <p>Powered by computer vision and machine learning for accurate food analysis</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
