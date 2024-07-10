# utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CENTRAL_LLM_URL = os.getenv('CENTRAL_LLM_URL', 'http://central-llm:5000')
    PRICE_PREDICTION_URL = os.getenv('PRICE_PREDICTION_URL', 'http://price-prediction:5001')
    CV_MODULE_URL = os.getenv('CV_MODULE_URL', 'http://cv-module:5002')
    
    SCRAPING_URLS = [
        "https://example.com/bitcoin",
        "https://example.com/runes",
        "https://example.com/ordinals"
    ]
    DATA_RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")