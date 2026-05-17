import os
import sys
from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self, model, preprocessor):
        try:
            self.model = model
            self.preprocessor = preprocessor
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def predict(self, X):
        """
        Predict output for any new data using the Preprocessor object created in Data Transformation
        """
        try:
            return self.model.predict(self.preprocessor.transform(X))
        except Exception as e:
            raise NetworkSecurityException(e, sys)