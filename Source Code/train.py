"""
HematoVision - Training Module
"""

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main training pipeline"""
    
    print("\n" + "="*80)
    print("HematoVision - Blood Cell Classification Training")
    print("="*80 + "\n")
    
    DATASET_PATH = 'dataset'
    
    # Check dataset
    if not Path(DATASET_PATH).exists():
        logger.error(f"Dataset not found at {DATASET_PATH}")
        print("\nPlease create dataset structure:")
        print(f"  {DATASET_PATH}/")
        print("    ├── Eosinophils/")
        print("    ├── Lymphocytes/")
        print("    ├── Monocytes/")
        print("    └── Neutrophils/")
        return
    
    logger.info("Training module initialized")
    logger.info("Download dataset from: https://www.kaggle.com/datasets/obulisainaren/blood-cell-images")

if __name__ == '__main__':
    main()