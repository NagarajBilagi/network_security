import os
import sys
import numpy as np
import pandas as pd


"""
Common consatnt variables for training pipeline
"""

TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH:str = os.path.join('data_schema', 'schema.yaml')

"""
Data ingestion related constant variable names
"""

DATA_INGESTION_COLLECTION_NAME : str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "NagarajAI"
DATA_INGESTION_DIR_NAME : str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "feature_Store"
DATA_INGESTION_INGESTED_DIR : str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

"""
Data validation related constant variable names
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "Invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

"""
Data trnaformation related constant variable names
"""

DATA_TRANSFORMATION_DIR_NAME: str ="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str ="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME : str= "preprocessing.pkl"

DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
"missing_values": np.nan,
"n_neighbors" : 3,
"weights": "uniform"}

"""
Model trainer related constant varible names
"""

MODEL_TRAINER_DIRECTORY_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_DIREACTORY:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD_SCORE:float = 0.05

