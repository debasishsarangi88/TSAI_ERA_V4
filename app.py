import streamlit as st
import cv2
import numpy as np
from PIL import Image
import requests
import json
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="🍽️ AI Food Ingredient Scanner",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4ECDC4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .upload-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
    }
    .result-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
    }
    .info-box {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
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

# Mock food recognition function (replace with actual AI model)
def recognize_food_items(image):
    """Mock function to recognize food items in image"""
    # This is a placeholder - replace with actual AI model
    mock_foods = [
        {"name": "Pizza Margherita", "confidence": 0.95, "ingredients": [
            "Flour", "Tomato sauce", "Mozzarella cheese", "Basil", "Olive oil", "Salt"
        ]},
        {"name": "Caesar Salad", "confidence": 0.87, "ingredients": [
            "Romaine lettuce", "Parmesan cheese", "Croutons", "Caesar dressing", "Black pepper"
        ]},
        {"name": "Pasta Carbonara", "confidence": 0.92, "ingredients": [
            "Spaghetti", "Eggs", "Pancetta", "Parmesan cheese", "Black pepper", "Salt"
        ]}
    ]
    return mock_foods

def get_nutrition_info(food_name):
    """Mock function to get nutrition information"""
    nutrition_data = {
        "Pizza Margherita": {"calories": 266, "protein": 11, "carbs": 33, "fat": 10},
        "Caesar Salad": {"calories": 94, "protein": 6, "carbs": 4, "fat": 7},
        "Pasta Carbonara": {"calories": 650, "protein": 25, "carbs": 71, "fat": 31}
    }
    return nutrition_data.get(food_name, {"calories": 0, "protein": 0, "carbs": 0, "fat": 0})

def main():
    # Header
    st.markdown('<h1 class="main-header">🍽️ AI Food Ingredient Scanner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload an image of your food and discover its ingredients!</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 App Statistics")
        st.metric("Total Scans", len(st.session_state.scan_history))
        st.metric("Today's Scans", len([s for s in st.session_state.scan_history 
                                      if s['timestamp'].date() == datetime.now().date()]))
        
        st.markdown("### 🔧 Settings")
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7, 0.05)
        
        st.markdown("### 📚 About")
        st.info("""
        This AI-powered app helps you:
        • Identify food items in images
        • Discover ingredients and nutritional info
        • Track your food scanning history
        • Make informed dietary choices
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### 📸 Upload Food Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of food items"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.session_state.uploaded_image = image
            
            # Scan button
            if st.button("🔍 Scan for Ingredients", type="primary"):
                with st.spinner("Analyzing image..."):
                    # Simulate processing time
                    import time
                    time.sleep(2)
                    
                    # Get food recognition results
                    results = recognize_food_items(image)
                    st.session_state.scan_results = results
                    
                    # Add to history
                    scan_record = {
                        'timestamp': datetime.now(),
                        'image_name': uploaded_file.name,
                        'foods_found': len(results),
                        'results': results
                    }
                    st.session_state.scan_history.append(scan_record)
                    
                    st.success("Scan completed! Check the results on the right.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if st.session_state.scan_results:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            st.markdown("### 🎯 Scan Results")
            
            for i, food in enumerate(st.session_state.scan_results):
                with st.expander(f"🍕 {food['name']} (Confidence: {food['confidence']:.1%})", expanded=True):
                    st.markdown("**Ingredients:**")
                    ingredients_df = pd.DataFrame({
                        'Ingredient': food['ingredients'],
                        'Category': ['Base', 'Sauce', 'Cheese', 'Herb', 'Oil', 'Seasoning'][:len(food['ingredients'])]
                    })
                    st.dataframe(ingredients_df, use_container_width=True)
                    
                    # Nutrition info
                    nutrition = get_nutrition_info(food['name'])
                    col_n1, col_n2, col_n3, col_n4 = st.columns(4)
                    with col_n1:
                        st.metric("Calories", f"{nutrition['calories']}")
                    with col_n2:
                        st.metric("Protein", f"{nutrition['protein']}g")
                    with col_n3:
                        st.metric("Carbs", f"{nutrition['carbs']}g")
                    with col_n4:
                        st.metric("Fat", f"{nutrition['fat']}g")
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.info("👆 Upload an image and click 'Scan for Ingredients' to get started!")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # History section
    if st.session_state.scan_history:
        st.markdown("### 📈 Scan History")
        
        # Create history dataframe
        history_data = []
        for record in st.session_state.scan_history:
            history_data.append({
                'Date': record['timestamp'].strftime('%Y-%m-%d %H:%M'),
                'Image': record['image_name'],
                'Foods Found': record['foods_found'],
                'Total Ingredients': sum(len(food['ingredients']) for food in record['results'])
            })
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Foods found over time
            fig_foods = px.line(
                history_df, 
                x='Date', 
                y='Foods Found',
                title="Foods Identified Over Time",
                markers=True
            )
            fig_foods.update_layout(showlegend=False)
            st.plotly_chart(fig_foods, use_container_width=True)
        
        with col_chart2:
            # Ingredients distribution
            all_ingredients = []
            for record in st.session_state.scan_history:
                for food in record['results']:
                    all_ingredients.extend(food['ingredients'])
            
            if all_ingredients:
                ingredient_counts = pd.Series(all_ingredients).value_counts().head(10)
                fig_ingredients = px.bar(
                    x=ingredient_counts.values,
                    y=ingredient_counts.index,
                    orientation='h',
                    title="Top 10 Most Common Ingredients"
                )
                st.plotly_chart(fig_ingredients, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🍽️ AI Food Ingredient Scanner | Built with Streamlit & AI</p>
        <p>Upload food images to discover ingredients and nutritional information</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
