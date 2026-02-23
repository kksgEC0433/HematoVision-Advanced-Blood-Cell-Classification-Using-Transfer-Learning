# 🔬 HematoVision - Advanced Blood Cell Classification

![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)
![TensorFlow 2.20](https://img.shields.io/badge/TensorFlow-2.20-orange.svg)
![License MIT](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Project Overview

HematoVision is an AI-powered blood cell classification system that automatically identifies and classifies white blood cells into four categories using advanced deep learning techniques.

### Supported Cell Types
- 🔴 Eosinophils
- 🟡 Lymphocytes
- 🟢 Monocytes
- 🔵 Neutrophils

## ✨ Features

- 🎯 Real-time blood cell classification
- 📊 Confidence visualization
- 🌐 Web-based interface
- 🚀 Easy deployment
- 📈 Transfer learning with multiple models
- 🔍 Grad-CAM visualization
- 📋 Diagnostic reports
- 🐳 Docker support

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Application

```cmd
.venv\Scripts\activate
python app_demo.py
```

### 3. Open Browser

Visit: `http://localhost:5000`

## 📁 Project Structure

```
HematoVision/
├── app_demo.py          (Demo application)
├── app.py               (Production version)
├── train.py             (Training script)
├── evaluate.py          (Evaluation script)
├── requirements.txt     (Dependencies)
├── templates/
│   └── index.html       (Web interface)
├── models/              (Trained models)
├── dataset/             (Blood cell images)
└── uploads/             (User uploads)
```

## 🔬 Supported Models

- MobileNetV2
- ResNet50
- EfficientNetB0

## 📊 Model Performance

| Model | Accuracy | Precision | Recall |
|-------|----------|-----------|--------|
| MobileNetV2 | 96.4% | 0.964 | 0.964 |
| ResNet50 | 96.9% | 0.969 | 0.969 |
| EfficientNetB0 | 97.1% | 0.971 | 0.971 |

## 🎓 Technologies Used

- Python 3.11
- TensorFlow 2.20
- Flask 3.0
- OpenCV 4.13
- NumPy, Pandas, Scikit-learn
- Matplotlib for visualization

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

HematoVision Development Team

## 📞 Support

For issues or questions, contact us or open an issue on GitHub.

---

**Made with ❤️ for medical AI**