from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException

from network_security.entity.config_entity import (TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, 
                                                   DataTransformationConfig, ModelTrainerConfig)

from network_security.entity.artifact_entity import (DataIngestionArtifact, DataValidationArtifact,
                                                     DataTransformationArtifact, ModelTrainerArtifact)

from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTranformation
from network_security.components.model_trainer import ModelTrainer

from network_security.cloud.s3_syncer import s3sync
from network_security.constant.training_pipeline import TRAINING_BUCKET_NAME

import os, sys


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3sync= s3sync()
        


    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            logging.info("Start data ingestion")
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info("Start data validation")
            data_validation_config = DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"data validation completed and artifact:  {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact):
        try:
            logging.info("Start data transformation")
            data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTranformation(data_validation_artifact, data_transformation_config )
            data_transformation_artifact = data_transformation.inintiate_data_transformation()
            logging.info(f"data transformation completed and artifact:  {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            logging.info("Start model trainer")
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
            model_trainer_artifact= model_trainer.initiate_model_trainer()
            logging.info(f"model trainer completed and artifact:  {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)   
        

    # local artifact going to s3 bucket
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifiact/{self.training_pipeline_config.timestamp}"
            self.s3sync.sync_folder_to_s3(folder= self.training_pipeline_config.artifact_dir, aws_bucket_url= aws_bucket_url)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    # local saved model going to s3 bucket
    def sync_saved_model_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3sync.sync_folder_to_s3(folder= self.training_pipeline_config.model_dir, aws_bucket_url= aws_bucket_url)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        try:
            
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)

            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_to_s3()
            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    






        
        