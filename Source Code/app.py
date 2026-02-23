"""
HematoVision - Production Application
Blood Cell Classification System with AI Model Support
"""

from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import json
from pathlib import Path
import io
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 16 * 1024 * 1024))
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Create directories
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Global variables
MODEL = None
CLASS_NAMES = ['Eosinophils', 'Lymphocytes', 'Monocytes', 'Neutrophils']
IMG_SIZE = 224

# Cell descriptions
CELL_DESCRIPTIONS = {
    'Eosinophils': {
        'description': 'Eosinophils are white blood cells that fight parasitic infections and allergic reactions.',
        'morphology': 'Bilobed nucleus, abundant pink/red granules in cytoplasm',
        'normal_range': '1-4% of white blood cells',
        'function': 'Defense against parasites and allergies'
    },
    'Lymphocytes': {
        'description': 'Lymphocytes are crucial for adaptive immunity and antibody production.',
        'morphology': 'Small cell, large nucleus, scanty cytoplasm',
        'normal_range': '20-40% of white blood cells',
        'function': 'Immune response and antibody production'
    },
    'Monocytes': {
        'description': 'Monocytes develop into macrophages to clear infections.',
        'morphology': 'Largest WBC, kidney-shaped nucleus, abundant gray cytoplasm',
        'normal_range': '2-8% of white blood cells',
        'function': 'Phagocytosis and antigen presentation'
    },
    'Neutrophils': {
        'description': 'Neutrophils are the most abundant white blood cells and first responders to infection.',
        'morphology': 'Multi-lobed nucleus, fine granules, pale cytoplasm',
        'normal_range': '40-60% of white blood cells',
        'function': 'Combat bacterial infections'
    }
}

def load_model(model_path=None):
    """Load pre-trained model"""
    global MODEL
    if MODEL is None:
        if model_path is None:
            model_path = os.getenv('MODEL_PATH', 'models/EfficientNetB0_best.h5')
        
        if not os.path.exists(model_path):
            logger.warning(f"Model not found at {model_path}")
            return False
        
        try:
            MODEL = keras.models.load_model(model_path)
            logger.info(f"Model loaded successfully: {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    return True

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def preprocess_image(image_path):
    """Preprocess image for prediction"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img / 255.0
        
        return np.expand_dims(img, axis=0)
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        return None

def predict_cell_type(image_path):
    """Predict blood cell type"""
    if MODEL is None:
        return None, None, None
    
    try:
        img_array = preprocess_image(image_path)
        if img_array is None:
            return None, None, None
        
        predictions = MODEL.predict(img_array, verbose=0)
        pred_class = np.argmax(predictions[0])
        confidence = float(predictions[0][pred_class])
        all_confidences = {CLASS_NAMES[i]: float(predictions[0][i]) for i in range(4)}
        
        return CLASS_NAMES[pred_class], confidence, all_confidences
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return None, None, None

def generate_diagnostic_report(predicted_class, confidence, all_confidences, filename):
    """Generate diagnostic report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = {
        'timestamp': timestamp,
        'filename': filename,
        'predicted_cell_type': predicted_class,
        'confidence': f"{confidence:.2%}",
        'all_predictions': {k: f"{v:.2%}" for k, v in all_confidences.items()},
        'cell_info': CELL_DESCRIPTIONS.get(predicted_class, {}),
        'recommendation': f"Predicted: {predicted_class} with {confidence:.1%} confidence"
    }
    
    if confidence < 0.7:
        report['warning'] = "⚠️ Low confidence prediction. Manual review recommended."
    
    return report

def create_confidence_chart(all_confidences):
    """Create confidence visualization"""
    try:
        fig, ax = plt.subplots(figsize=(8, 6))
        
        classes = list(all_confidences.keys())
        scores = list(all_confidences.values())
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        
        bars = ax.bar(classes, scores, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
        ax.set_ylabel('Confidence', fontsize=12, fontweight='bold')
        ax.set_title('Blood Cell Classification Confidence', fontsize=14, fontweight='bold')
        ax.set_ylim([0, 1])
        ax.grid(True, alpha=0.3, axis='y')
        
        for bar, score in zip(bars, scores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{score:.1%}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        logger.error(f"Error creating chart: {e}")
        return None

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for prediction"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Use: png, jpg, jpeg'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Predict
        predicted_class, confidence, all_confidences = predict_cell_type(filepath)
        
        if predicted_class is None:
            return jsonify({'error': 'Failed to process image'}), 500
        
        # Generate report
        report = generate_diagnostic_report(predicted_class, confidence, all_confidences, filename)
        
        # Create chart
        chart_base64 = create_confidence_chart(all_confidences)
        
        return jsonify({
            'success': True,
            'predicted_cell': predicted_class,
            'confidence': f"{confidence:.2%}",
            'all_predictions': {k: f"{v:.2%}" for k, v in all_confidences.items()},
            'report': report,
            'chart': chart_base64,
            'uploaded_file': filename
        }), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/info/<cell_type>')
def cell_info(cell_type):
    """Get information about cell type"""
    if cell_type not in CLASS_NAMES:
        return jsonify({'error': 'Invalid cell type'}), 400
    return jsonify(CELL_DESCRIPTIONS.get(cell_type, {})), 200

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model_loaded': MODEL is not None,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    if load_model():
        logger.info("✓ Flask app initialized successfully")
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        app.run(debug=True, host=host, port=port)
    else:
        logger.error("✗ Failed to load model")