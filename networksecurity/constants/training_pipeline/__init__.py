import os
import sys
import numpy as np
import pandas as pd


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