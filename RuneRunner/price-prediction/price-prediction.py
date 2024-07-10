import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging
import os
import json

from src.models.linear_regression import LinearRegressionModel
from utils.config import Config
from utils.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

class PricePrediction:
    def __init__(self):
        self.config = Config()
        self.model = LinearRegressionModel()
        self.scaler = StandardScaler()

    def load_data(self):
        """
        Lädt die gescrapten Daten aus dem DATA_RAW_DIR.
        """
        data_files = [f for f in os.listdir(self.config.DATA_RAW_DIR) if f.endswith('.json')]
        if not data_files:
            logger.warning(f"Keine Datendateien in {self.config.DATA_RAW_DIR} gefunden.")
            return None
        
        data_list = []
        for file in data_files:
            try:
                with open(os.path.join(self.config.DATA_RAW_DIR, file), 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        data_list.extend(data)
                    else:
                        data_list.append(data)
            except json.JSONDecodeError:
                logger.error(f"Fehler beim Lesen der Datei {file}. Überspringe diese Datei.")
                continue
        
        if not data_list:
            logger.warning("Keine gültigen Daten in den Dateien gefunden.")
            return None
        
        return pd.DataFrame(data_list)

    def prepare_features(self, data):
        """
        Bereitet die Features für das Modell vor.
        """
        if data is None or data.empty:
            logger.error("Keine Daten zum Vorbereiten der Features vorhanden.")
            return None, None

        # Beispiel: Verwendung von 'price' als Zielwert und andere numerische Spalten als Features
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        if 'price' not in numeric_columns:
            logger.error("'price' Spalte nicht in den Daten gefunden oder nicht numerisch.")
            return None, None

        features = data[numeric_columns].drop('price', axis=1)
        target = data['price']

        # Behandle fehlende Werte
        features = features.fillna(features.mean())
        target = target.fillna(target.mean())

        # Normalisiere die Features
        features_scaled = self.scaler.fit_transform(features)

        return features_scaled, target

    def train_model(self, features, target):
        """
        Trainiert das lineare Regressionsmodell.
        """
        if features is None or target is None:
            logger.error("Keine gültigen Features oder Zielwerte zum Trainieren des Modells.")
            return

        self.model.train(features, target)

    def make_prediction(self, features):
        """
        Macht eine Vorhersage mit dem trainierten Modell.
        """
        if features is None:
            logger.error("Keine gültigen Features für die Vorhersage.")
            return None

        return self.model.predict(features)

    def run(self):
        """
        Führt den gesamten Prozess aus: Daten laden, Features vorbereiten, 
        Modell trainieren und Vorhersage machen.
        """
        logger.info("Starting price prediction process")
        
        # Lade Daten
        data = self.load_data()
        if data is None:
            logger.error("Konnte keine Daten laden. Beende den Prozess.")
            return None

        logger.info(f"Loaded {len(data)} data points")

        # Bereite Features vor
        features, target = self.prepare_features(data)
        if features is None or target is None:
            logger.error("Konnte keine Features vorbereiten. Beende den Prozess.")
            return None

        logger.info(f"Prepared features with shape {features.shape}")

        # Trainiere Modell
        self.train_model(features, target)

        # Mache Vorhersage für den nächsten Tag
        if features.shape[0] > 0:
            last_features = features[-1].reshape(1, -1)
            prediction = self.make_prediction(last_features)
            if prediction is not None:
                logger.info(f"Prediction for next day: {prediction[0]}")
            else:
                logger.error("Konnte keine Vorhersage machen.")
                return None
        else:
            logger.error("Nicht genug Daten für eine Vorhersage.")
            return None

        # Speichere das Modell
        model_path = os.path.join(self.config.DATA_PROCESSED_DIR, 'linear_regression_model.joblib')
        self.model.save_model(model_path)
        logger.info(f"Model saved to {model_path}")

        return prediction[0] if prediction is not None else None

if __name__ == "__main__":
    config = Config()
    price_predictor = PricePrediction(config)
    predicted_price = price_predictor.run()
    if predicted_price is not None:
        print(f"Predicted price for next day: {predicted_price}")
    else:
        print("Konnte keine Vorhersage machen aufgrund von Datenmangel oder Fehlern.")
