import logging
import os
from datetime import datetime

def setup_logger():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure logging
    log_filename = f'logs/real_estate_agent_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    # Set up logging format
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure the root logger
    logging.basicConfig(
        level=logging.INFO,
        format=logging_format,
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('RealEstateAgent')
