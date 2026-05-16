import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

# Data ingestion variables
DATA_INGESTION_COLLECTION_NAME: str = "NETWORK_COLLECTION"
DATA_INGESTION_DATABASE_NAME: str = "NETWORK_SECURITY_DB"
DATA_INGESTION_DIRECTORY_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIRECTORY: str = "feature_store"
DATA_INGESTION_INGESTED_DIRECTORY: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

# Constant Variables for training pipeline
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"


# Data validation variables
DATA_VALIDATION_DIRECTORY_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIRECTORY: str = "validated"
DATA_VALIDATION_INVALID_DIRECTORY: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIRECTORY: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = f"report_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.html"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"