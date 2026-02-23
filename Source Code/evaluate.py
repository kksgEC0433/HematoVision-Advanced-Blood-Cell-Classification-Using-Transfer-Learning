"""
HematoVision - Model Evaluation Module
"""

import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main evaluation"""
    print("\n" + "="*80)
    print("HematoVision - Model Evaluation")
    print("="*80 + "\n")
    
    logger.info("Evaluation module ready")
    logger.info("To evaluate models, use trained models from 'models/' folder")

if __name__ == '__main__':
    main()