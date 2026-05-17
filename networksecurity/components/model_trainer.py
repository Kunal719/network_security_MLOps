import sys
import os
from networksecurity.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact, ClassificationMetricArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.metrics import f1_score, precision_score, recall_score, r2_score

from networksecurity.utils.main_utils.utils import save_object, load_object, load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metrics.classification_metric import get_classification_report
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(verbose=1),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
                "KNN": KNeighborsClassifier(),
            }
            
            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                'criterion':['gini', 'entropy', 'log_loss'],     
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            },
            "KNN":{
                'n_neighbors':[5,7,9,11],
                'weights':['uniform','distance'],
                # 'algorithm':['auto','ball_tree','kd_tree','brute']
            }
        }
            
            logging.info("Training started")
            model_report, best_models =evaluate_models(X_train, y_train, X_test, y_test, models,params)
            
            best_model_score = max((model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = best_models[best_model_name]
            
            logging.info(f"Predicting on training data with the best model : {best_model_name}")
            y_train_pred = best_model.predict(X_train)

            logging.info("Getting the classification report for Training Data")
            classification_train_metric: ClassificationMetricArtifact = get_classification_report(y_true=y_train, y_pred=y_train_pred)

            logging.info("Predicting on test data with the best model")
            y_test_pred = best_model.predict(X_test)

            logging.info("Getting the classification report for Test Data")
            classification_test_metric: ClassificationMetricArtifact = get_classification_report(y_true=y_test, y_pred=y_test_pred)

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)

            os.makedirs(model_dir_path, exist_ok=True)

            network_model = NetworkModel(model=best_model, preprocessor=preprocessor)
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)

            # Model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Load the data
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)