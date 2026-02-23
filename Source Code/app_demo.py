"""
HematoVision - DEMO MODE Application
Blood Cell Classification System
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
import os
import base64
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fix matplotlib backend BEFORE importing pyplot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Initialize Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Create directories
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Constants
CLASS_NAMES = ['Eosinophils', 'Lymphocytes', 'Monocytes', 'Neutrophils']

# Cell Information
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

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def simulate_prediction(filename):
    """Simulate AI prediction"""
    hash_value = hash(filename) % 100
    
    if hash_value < 25:
        pred_class = 0
    elif hash_value < 50:
        pred_class = 1
    elif hash_value < 75:
        pred_class = 2
    else:
        pred_class = 3
    
    np.random.seed(hash_value)
    confidences = np.random.dirichlet(np.ones(4)) * 0.3 + np.array([0.2, 0.2, 0.2, 0.2])
    confidences[pred_class] = np.random.uniform(0.75, 0.98)
    confidences = confidences / confidences.sum()
    
    return CLASS_NAMES[pred_class], float(confidences[pred_class]), {CLASS_NAMES[i]: float(confidences[i]) for i in range(4)}

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
        plt.close(fig)
        
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
    """Prediction endpoint"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        predicted_class, confidence, all_confidences = simulate_prediction(filename)
        
        report = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'filename': filename,
            'predicted_cell_type': predicted_class,
            'confidence': f"{confidence:.2%}",
            'all_predictions': {k: f"{v:.2%}" for k, v in all_confidences.items()},
            'cell_info': CELL_DESCRIPTIONS.get(predicted_class, {}),
            'recommendation': f"Predicted: {predicted_class} with {confidence:.1%} confidence"
        }
        
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
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'mode': 'DEMO',
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🔬 HematoVision - DEMO MODE")
    print("="*70)
    print("✅ Application initialized")
    print("✅ Open: http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)