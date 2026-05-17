import os
import sys
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import pickle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV

def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Executing save_object method of main_utils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of main_utils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}
        best_models = {}

        for model_name, model in models.items():

            para = param[model_name]

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            best_model = gs.best_estimator_

            best_model.fit(X_train, y_train)

            y_test_pred = best_model.predict(X_test)

            test_model_score = accuracy_score(y_test, y_test_pred)

            report[model_name] = test_model_score
            best_models[model_name] = best_model

        return report, best_models

    except Exception as e:
        raise NetworkSecurityException(e, sys)