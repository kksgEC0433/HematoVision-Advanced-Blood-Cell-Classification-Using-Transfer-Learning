# 🔧 HematoVision - Setup Guide

## System Requirements

- Python 3.9+
- pip 21.0+
- 2GB RAM minimum
- 1GB disk space

## Installation Steps

### Step 1: Install Python

Download from: https://www.python.org/downloads/

**IMPORTANT:** Check ✅ "Add Python to PATH"

### Step 2: Create Project Folder

```cmd
mkdir HematoVision
cd HematoVision
```

### Step 3: Create Virtual Environment

```cmd
python -m venv .venv
```

### Step 4: Activate Virtual Environment

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

You should see: `(.venv)` at the start of terminal

### Step 5: Install Dependencies

```cmd
pip install -r requirements.txt
```

Wait 10-15 minutes for installation...

### Step 6: Run Application

```cmd
python app_demo.py
```

### Step 7: Open in Browser

Visit: `http://localhost:5000`

## Troubleshooting

### Port 5000 Already in Use

Edit `app_demo.py`:
```python
app.run(port=5001)  # Change to 5001
```

### Module Not Found

```cmd
pip install -r requirements.txt --upgrade
```

### TensorFlow Installation Issues

```cmd
pip install tensorflow --upgrade
```

## Next Steps

1. Upload blood cell images
2. View AI predictions
3. Explore confidence scores
4. Train your own models (optional)

---

For detailed usage, see: README.md