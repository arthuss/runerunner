import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import logging
import os
import sys

# Fügen Sie den Projektroot zum Python-Pfad hinzu
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.models.linear_regression import LinearRegressionModel
from utils.config import Config
from utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

class PricePrediction:
    def __init__(self, config):
        self.config = config
        self.model = LinearRegressionModel()
        self.scaler = StandardScaler()

    def load_data(self):
        """
        Lädt die gescrapten Daten aus dem DATA_RAW_DIR.
        Hier sollten Sie die Logik implementieren, um Ihre spezifischen Datendateien zu laden.
        """
        data_files = [f for f in os.listdir(self.config.DATA_RAW_DIR) if f.endswith('.json')]
        data_list = []
        for file in data_files:
            with open(os.path.join(self.config.DATA_RAW_DIR, file), 'r') as f:
                data = pd.read_json(f)
                data_list.append(data)
        
        return pd.concat(data_list, ignore_index=True)

    def prepare_features(self, data):
        """
        Bereitet die Features für das Modell vor.
        Diese Funktion sollte an Ihre spezifischen Daten angepasst werden.
        """
        # Beispiel: Verwendung von 'price' als Zielwert und andere Spalten als Features
        features = data.drop(['price', 'timestamp'], axis=1, errors='ignore')
        target = data['price']

        # Konvertiere kategorische Variablen
        features = pd.get_dummies(features)

        # Normalisiere die Features
        features_scaled = self.scaler.fit_transform(features)

        return features_scaled, target

    def train_model(self, features, target):
        """
        Trainiert das lineare Regressionsmodell.
        """
        self.model.train(features, target)

    def make_prediction(self, features):
        """
        Macht eine Vorhersage mit dem trainierten Modell.
        """
        return self.model.predict(features)

    def run(self):
        """
        Führt den gesamten Prozess aus: Daten laden, Features vorbereiten, 
        Modell trainieren und Vorhersage machen.
        """
        logger.info("Starting price prediction process")
        
        # Lade Daten
        data = self.load_data()
        logger.info(f"Loaded {len(data)} data points")

        # Bereite Features vor
        features, target = self.prepare_features(data)
        logger.info(f"Prepared features with shape {features.shape}")

        # Trainiere Modell
        self.train_model(features, target)

        # Mache Vorhersage für den nächsten Tag
        last_features = features[-1].reshape(1, -1)
        prediction = self.make_prediction(last_features)
        
        logger.info(f"Prediction for next day: {prediction[0]}")

        # Speichere das Modell
        model_path = os.path.join(self.config.DATA_PROCESSED_DIR, 'linear_regression_model.joblib')
        self.model.save_model(model_path)
        logger.info(f"Model saved to {model_path}")

        return prediction[0]

if __name__ == "__main__":
    config = Config()
    price_predictor = PricePrediction(config)
    predicted_price = price_predictor.run()
    print(f"Predicted price for next day: {predicted_price}")