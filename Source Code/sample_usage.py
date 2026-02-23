"""
HematoVision - Sample Usage Script
Test the application
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLASS_NAMES = ['Eosinophils', 'Lymphocytes', 'Monocytes', 'Neutrophils']

def main():
    print("\n" + "="*60)
    print("HematoVision - Sample Usage")
    print("="*60 + "\n")
    
    logger.info("HematoVision is ready!")
    logger.info(f"Supported cell types: {', '.join(CLASS_NAMES)}")
    logger.info("Run: python app_demo.py")
    logger.info("Then visit: http://localhost:5000")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()