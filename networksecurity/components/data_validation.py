from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.schema.schema_validation import data_schema_validation
import sys
import os
import pandas as pd
import pandera.pandas as pa
from pandera.errors import SchemaErrors
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from datetime import datetime

# print(data_schema_validation)

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    @staticmethod
    def validate_schema(dataframe: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        try:
            validated_df = data_schema_validation.validate(dataframe, lazy=True)
            logging.info(f"{dataset_name} schema validation successful")
            return validated_df

        except SchemaErrors as e:
            logging.error(f"{dataset_name} schema validation failed")
            logging.error(str(e))
            logging.error(f"\nFailure Cases:\n{e.failure_cases}")
            raise NetworkSecurityException(e, sys)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def detect_data_drift(self, reference_df: pd.DataFrame, cuurent_df: pd.DataFrame) -> bool:
        try:
            logging.info("Starting data drift detection")

            report = Report(metrics=[DataDriftPreset()])
            report.run(reference_data=reference_df, current_data=cuurent_df)

            drift_report_dir = os.path.dirname(self.data_validation_config.drift_report_file_path)
            os.makedirs(drift_report_dir, exist_ok=True)

            # Save report
            report.save_html(self.data_validation_config.drift_report_file_path)

            logging.info(f"Drift report saved at: {self.data_validation_config.drift_report_file_path}")

            drift_result = report.as_dict()

            # Extract Drift Metrics
            drift_detected = drift_result["metrics"][0]["result"]["dataset_drift"]
            n_drift_columns = drift_result["metrics"][0]["result"]["number_of_drifted_columns"]
            total_cols = drift_result["metrics"][0]["result"]["number_of_columns"]

            logging.info(f"Drift detected: {drift_detected}")
            logging.info(f"Number of drifted columns: {n_drift_columns} / {total_cols}")

            return drift_detected
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Read data from train and test file
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            # Validate Train input schema
            validated_train_df = DataValidation.validate_schema(train_df, "Train Dataset")

            # Validate Test input schema
            validated_test_df = DataValidation.validate_schema(test_df, "Test Dataset")

            # Detect Data drift
            drift_detected = self.detect_data_drift(reference_df=validated_train_df, cuurent_df=validated_test_df)

            # Create Validated Data Directory
            os.makedirs(self.data_validation_config.valid_data_dir,exist_ok=True)

            # Create Invalid Data Directory
            os.makedirs(self.data_validation_config.invalid_data_dir,exist_ok=True)

            validated_train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            validated_test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            # Artifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=drift_detected,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact
        except Exception as e:  
            raise NetworkSecurityException(e, sys)
