# ⚡ HematoVision - Quick Start (5 Minutes)

## Step 1: Open Command Prompt

Press `Win + R`, type `cmd`, press Enter

## Step 2: Navigate to Project

```cmd
cd D:\VS Code Projects\HematoVision
```

(Use your actual path)

## Step 3: Activate Virtual Environment

```cmd
.venv\Scripts\activate
```

You should see: `(.venv)` at start

## Step 4: Install Dependencies (First Time Only)

```cmd
pip install -r requirements.txt
```

Wait 10 minutes...

## Step 5: Run Application

```cmd
python app_demo.py
```

You should see:
```
======================================================================
🔬 HematoVision - DEMO MODE
======================================================================
✅ All dependencies installed
✅ Open browser to: http://localhost:5000
✅ Upload blood cell images to test
======================================================================

 * Serving Flask app 'app_demo'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

## Step 6: Open Browser

Visit: **`http://localhost:5000`** 🎉

## Step 7: Test Application

1. Click upload area
2. Select any image (JPG, PNG)
3. View AI prediction
4. See confidence scores

## Troubleshooting

**Port 5000 in use?**
Edit `app_demo.py`, change `port=5000` to `port=5001`

**Module not found?**
```cmd
pip install -r requirements.txt --upgrade
```

**Virtual environment won't activate?**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

## Next Steps

- ✅ Train models: `python train.py`
- ✅ Evaluate models: `python evaluate.py`
- ✅ Test sample: `python sample_usage.py`

---

**That's it! You're running HematoVision!** 🚀