from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException

from network_security.entity.config_entity import DataValidationConfig, DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from network_security.constant.training_pipeline import SCHEMA_FILE_PATH
from network_security.utils.main_utils.utils import read_yaml_file, write_yaml_file
import os
import sys
import numpy as np
import pandas as pd
import pymongo 

from scipy.stats import ks_2samp

from dotenv import load_dotenv
load_dotenv()

MONGODBURL = os.getenv('MONGO_DB_URL')


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config:DataValidationConfig):

        try:
            self.data_ingestion_artifact =data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod   
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def validate_number_of_columns(self,data_frame:pd.DataFrame)-> bool:

        try:
            number_of_colmuns = len(self.schema_config['columns'])
            df_legth = len(data_frame.columns)
            logging.info(f"required number of columns in dataframe : {number_of_colmuns}")
            logging.info(f"number of columns present in dataframe : {df_legth}")
            if df_legth == number_of_colmuns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_data_drift(self, base_df, current_df, threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                base_data= base_df[column]
                current_data = current_df[column]
                is_same_dist = ks_2samp(base_data,current_data)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status =False

                report.update({column:
                               {'p_value':float(is_same_dist.pvalue),
                               'drift_status' :is_found }
                               })
            
            drift_report_file_path =self.data_validation_config.drift_report_file_path
            dir_path =os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path)
            write_yaml_file(file_path=drift_report_file_path, content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_validation(self):
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            #read dataset
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)


            # validate number of columns in train-test dataframe 
            status= self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message = f"train dataframe does not contain all the columns"
            
            status= self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"test dataframe does not contain all the columns"

            #data drift validation
            status =self.validate_data_drift(base_df= train_dataframe, current_df= test_dataframe)
            dir_path =os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok= True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index = False, header= True)

            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index = False, header= True)

            data_validation_artifact = DataValidationArtifact(
                validation_status= status,
                valid_train_file_path= self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path= self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path= None,
                invalid_test_file_path= None,
                drift_report_file_path= self.data_validation_config.drift_report_file_path

            ) 

            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)



