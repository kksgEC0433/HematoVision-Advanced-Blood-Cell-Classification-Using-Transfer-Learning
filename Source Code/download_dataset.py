"""
Download blood cell dataset
Run: python download_dataset.py
"""

import os
from pathlib import Path
import urllib.request
import zipfile

print("\n" + "="*70)
print("HematoVision - Dataset Downloader")
print("="*70 + "\n")

# Create dataset folder
dataset_path = Path('dataset')
dataset_path.mkdir(exist_ok=True)

# Create subfolders
classes = ['Eosinophils', 'Lymphocytes', 'Monocytes', 'Neutrophils']
for class_name in classes:
    (dataset_path / class_name).mkdir(exist_ok=True)

print("✅ Dataset folders created!")
print("\nFolder structure:")
for class_name in classes:
    folder_path = dataset_path / class_name
    print(f"  ✓ {folder_path}")

print("\n" + "="*70)
print("NEXT STEPS:")
print("="*70)
print("""
1. Download dataset from:
   - Kaggle: https://www.kaggle.com/datasets/obulisainaren/blood-cell-images
   - Or GitHub: https://github.com/maelfabien/Blood-Cell-Images

2. Extract the ZIP file

3. Copy images to folders:
   - Copy EOSINOPHIL images to: dataset/Eosinophils/
   - Copy LYMPHOCYTE images to: dataset/Lymphocytes/
   - Copy MONOCYTE images to: dataset/Monocytes/
   - Copy NEUTROPHIL images to: dataset/Neutrophils/

4. Verify with: python verify_dataset.py

5. Train models with: python train.py
""")

print("="*70 + "\n")