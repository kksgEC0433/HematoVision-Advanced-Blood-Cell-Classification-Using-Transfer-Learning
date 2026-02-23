# 📖 HematoVision - Usage Guide

## 🌐 Web Interface

### Uploading Images

1. **Open Browser:** `http://localhost:5000`
2. **Upload Image:** Click upload area or drag-and-drop
3. **View Results:** See predictions and confidence scores

### Supported Formats

- PNG
- JPG
- JPEG
- Max size: 16MB

### Understanding Results

**Confidence Score:** How confident the AI is (0-100%)

**Confidence Breakdown:** Probability for each cell type

## 🏋️ Training Models

Requires dataset with blood cell images in:
```
dataset/
├── Eosinophils/
├── Lymphocytes/
├── Monocytes/
└── Neutrophils/
```

Run training:
```cmd
python train.py
```

## 📊 Evaluating Models

```cmd
python evaluate.py
```

Generates:
- Confusion matrices
- Classification reports
- ROC curves
- Performance visualizations

## 🧪 Testing

```cmd
python sample_usage.py
```

## 📈 API Endpoints

### POST /predict
Upload image and get prediction

**Request:**
```
multipart/form-data
file: <image>
```

**Response:**
```json
{
  "success": true,
  "predicted_cell": "Lymphocytes",
  "confidence": "92%",
  "all_predictions": {...},
  "chart": "<base64_image>",
  "report": {...}
}
```

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "timestamp": "2026-02-21T16:50:00"
}
```

## 🎨 Customization

### Change Port

Edit `app_demo.py`:
```python
app.run(port=5001)
```

### Change Model

Edit `.env`:
```
MODEL_PATH=models/ResNet50_best.h5
```

## 📝 Logging

Logs appear in terminal showing:
- File uploads
- Predictions
- Errors
- Performance metrics

---

For setup instructions, see: SETUP_GUIDE.md