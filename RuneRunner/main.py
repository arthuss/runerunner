import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

def get_market_data():
    # Implementieren Sie hier die Logik zum Abrufen von Marktdaten
    pass

def analyze_market():
    market_data = get_market_data()
    try:
        response = requests.post('http://central-llm:5000/analyze', json={'market_data': market_data}, timeout=10)
        response.raise_for_status()
        return response.json()['analysis']
    except requests.RequestException as e:
        print(f"Fehler bei der Verbindung zum central-llm Service: {e}")
        return None

def predict_price():
    try:
        response = requests.post('http://price-prediction:5001/predict', timeout=10)
        response.raise_for_status()
        return response.json()['prediction']
    except requests.RequestException as e:
        print(f"Fehler bei der Verbindung zum price-prediction Service: {e}")
        return None

def main_loop():
    while True:
        market_analysis = analyze_market()
        if market_analysis:
            print(f"Market Analysis: {market_analysis}")
        
        price_prediction = predict_price()
        if price_prediction:
            print(f"Price Prediction: {price_prediction}")
        
        # Implementieren Sie hier Ihre Handelslogik
        
        time.sleep(60)  # Warten Sie eine Minute vor der nächsten Iteration

if __name__ == '__main__':
    main_loop()