import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import logging

logger = logging.getLogger(__name__)

class LinearRegressionModel:
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False

    def train(self, X, y):
        """
        Train the linear regression model.
        
        :param X: Features (2D array-like)
        :param y: Target variable (1D array-like)
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        logger.info(f"Model trained. MSE: {mse:.4f}, R2 Score: {r2:.4f}")

    def predict(self, X):
        """
        Make predictions using the trained model.
        
        :param X: Features to predict on (2D array-like)
        :return: Predicted values
        """
        if not self.is_trained:
            raise ValueError("Model is not trained yet. Call train() first.")
        return self.model.predict(X)

    def save_model(self, filepath):
        """
        Save the trained model to a file.
        
        :param filepath: Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Model is not trained yet. Call train() first.")
        joblib.dump(self.model, filepath)
        logger.info(f"Model saved to {filepath}")

    def load_model(self, filepath):
        """
        Load a trained model from a file.
        
        :param filepath: Path to the saved model
        """
        self.model = joblib.load(filepath)
        self.is_trained = True
        logger.info(f"Model loaded from {filepath}")

# Example usage
if __name__ == "__main__":
    # Generate some dummy data
    np.random.seed(0)
    X = np.random.rand(100, 3)  # 100 samples, 3 features
    y = 2 * X[:, 0] + 3 * X[:, 1] - X[:, 2] + np.random.randn(100) * 0.1

    model = LinearRegressionModel()
    model.train(X, y)

    # Make a prediction
    new_data = np.array([[0.5, 0.5, 0.5]])
    prediction = model.predict(new_data)
    print(f"Prediction for {new_data}: {prediction}")

    # Save and load the model
    model.save_model("linear_regression_model.joblib")
    new_model = LinearRegressionModel()
    new_model.load_model("linear_regression_model.joblib")

    # Verify the loaded model
    new_prediction = new_model.predict(new_data)
    print(f"Prediction with loaded model: {new_prediction}")