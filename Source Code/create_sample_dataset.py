"""
Create sample blood cell images for testing
Run: python create_sample_dataset.py
"""

import numpy as np
from PIL import Image
from pathlib import Path
import os

print("\n" + "="*70)
print("Creating Sample Blood Cell Images")
print("="*70 + "\n")

dataset_path = Path('dataset')
dataset_path.mkdir(exist_ok=True)

classes = ['Eosinophils', 'Lymphocytes', 'Monocytes', 'Neutrophils']

# Create 50 sample images per class
for class_idx, class_name in enumerate(classes):
    class_path = dataset_path / class_name
    class_path.mkdir(exist_ok=True)
    
    print(f"Creating {class_name} samples...")
    
    for i in range(50):
        # Create random image (simulate blood cell)
        img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # Add some patterns to differentiate cells
        if class_idx == 0:  # Eosinophils - red pattern
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] + 50, 0, 255)
        elif class_idx == 1:  # Lymphocytes - blue pattern
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] + 50, 0, 255)
        elif class_idx == 2:  # Monocytes - green pattern
            img_array[:, :, 1] = np.clip(img_array[:, :, 1] + 50, 0, 255)
        else:  # Neutrophils - mixed
            img_array = np.clip(img_array + 30, 0, 255)
        
        # Save image
        img = Image.fromarray(img_array.astype('uint8'))
        img_path = class_path / f'{class_name}_{i:04d}.jpg'
        img.save(img_path)
    
    print(f"  ✓ Created 50 images for {class_name}")

print("\n" + "="*70)
print("✅ Sample dataset created successfully!")
print("="*70 + "\n")

# Verify
print("Dataset structure:")
for class_name in classes:
    class_path = dataset_path / class_name
    count = len(list(class_path.glob('*.jpg')))
    print(f"  {class_name}: {count} images")

print("\n")