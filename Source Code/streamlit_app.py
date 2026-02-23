"""
HematoVision - Streamlit Alternative Interface
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="HematoVision", layout="wide", initial_sidebar_state="expanded")

# Styling
st.markdown("""
    <style>
        .main { padding: 0rem 0rem; }
        .css-1d391kg { padding: 2rem 1rem 10rem 1rem; }
    </style>
""", unsafe_allow_html=True)

# Configuration
MODEL_PATH = 'models/EfficientNetB0_best.h5'
IMG_SIZE = 224
CLASS_NAMES = ['Eosinophils', 'Lymphocytes', 'Monocytes', 'Neutrophils']
COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

CELL_INFO = {
    'Eosinophils': {
        'description': 'Fight parasitic infections and allergic reactions',
        'normal_range': '1-4%'
    },
    'Lymphocytes': {
        'description': 'Crucial for immune response and antibody production',
        'normal_range': '20-40%'
    },
    'Monocytes': {
        'description': 'Clear infections through phagocytosis',
        'normal_range': '2-8%'
    },
    'Neutrophils': {
        'description': 'Primary defense against bacteria',
        'normal_range': '40-60%'
    }
}

@st.cache_resource
def load_model():
    return keras.models.load_model(MODEL_PATH)

def main():
    # Header
    st.markdown("# 🔬 HematoVision")
    st.markdown("### Advanced Blood Cell Classification Using AI")
    
    # Sidebar
    st.sidebar.markdown("## Configuration")
    uploaded_file = st.sidebar.file_uploader("Upload Blood Cell Image", type=['jpg', 'jpeg', 'png'])
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("## Upload Image")
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
    
    with col2:
        st.markdown("## Results")
        if uploaded_file:
            # Load model
            model = load_model()
            
            # Preprocess
            image_np = np.array(Image.open(uploaded_file))
            image_np = cv2.resize(image_np, (IMG_SIZE, IMG_SIZE))
            image_np = image_np / 255.0
            image_batch = np.expand_dims(image_np, axis=0)
            
            # Predict
            predictions = model.predict(image_batch, verbose=0)
            pred_class_idx = np.argmax(predictions[0])
            confidence = predictions[0][pred_class_idx]
            
            # Display results
            st.markdown(f"### **{CLASS_NAMES[pred_class_idx]}**")
            st.markdown(f"**Confidence:** {confidence:.2%}")
            
            # Chart
            fig, ax = plt.subplots()
            ax.bar(CLASS_NAMES, predictions[0], color=COLORS, alpha=0.8)
            ax.set_ylabel('Probability')
            ax.set_ylim([0, 1])
            st.pyplot(fig)
            
            # Info
            cell_type = CLASS_NAMES[pred_class_idx]
            info = CELL_INFO.get(cell_type, {})
            st.markdown(f"**Description:** {info.get('description', 'N/A')}")
            st.markdown(f"**Normal Range:** {info.get('normal_range', 'N/A')}")

if __name__ == '__main__':
    main()