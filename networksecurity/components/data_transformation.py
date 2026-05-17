import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationArtifact):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def get_data_transformer_object(cls) -> Pipeline:
        logging.info("Get data transformer object method of DataTransformation class")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Initialised KNN imputer with params: %s", DATA_TRANSFORMATION_IMPUTER_PARAMS)

            pipeline = Pipeline(steps=[('imputer', imputer)])
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info('Starting data transformation')
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # Separating input features from target feature for Testing data
            input_train_features = train_df.drop(TARGET_COLUMN, axis=1)
            target_train_features = train_df[TARGET_COLUMN]

            # Replace -1 with 0 in target as output is only 1 & -1
            target_train_features.replace(-1, 0, inplace=True)

            # Separating input features from target feature for Training data
            input_test_features = test_df.drop(TARGET_COLUMN, axis=1)
            target_test_features = test_df[TARGET_COLUMN]

            # Replace -1 with 0 in target as output is only 1 & -1
            target_test_features.replace(-1, 0, inplace=True)

            # Get preprocessor object
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_train_features)

            # Fit preprocessor on train data
            transformed_input_train_features = preprocessor_object.transform(input_train_features)

            # Fit preprocessor on test data
            transformed_input_test_features = preprocessor_object.transform(input_test_features)

            train_arr = np.c_[transformed_input_train_features, np.array(target_train_features)]
            test_arr = np.c_[transformed_input_test_features, np.array(target_test_features)]

            # Save numpy array dataset
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)

            # Save preprocessor object
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            # Save preprocessor object to final_models location
            save_object("final_models/preprocessor.pkl", preprocessor_object)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            return data_transformation_artifact


        except Exception as e:
            raise NetworkSecurityException(e, sys)