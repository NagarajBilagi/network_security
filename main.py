from network_security.components.data_ingestion import DataIngestion
from network_security.entity.artifact_entity import DataIngestionArtifact
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.config_entity import TrainingPipelineConfig

from network_security.components.data_validation import DataValidation
from network_security.entity.config_entity import DataValidationConfig

from network_security.components.data_transformation import DataTranformation
from network_security.entity.config_entity import DataTransformationConfig

from network_security.components.model_trainer import ModelTrainer
from network_security.components.model_trainer import ModelTrainerConfig

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

import sys

if __name__ == "__main__":

    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config =DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info('initiate data ingestion')
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info('data ingestion completed')
        print(data_ingestion_artifact)

        data_validation_config =DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info('initiate data validation')
        data_validation_arifact = data_validation.initiate_data_validation()
        logging.info('data validation completed')
        print('data_validation_arifact :',data_validation_arifact)

        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTranformation(data_validation_arifact, data_transformation_config=data_transformation_config)
        logging.info("initiate data transformation")
        data_tranformation_artifact = data_transformation.inintiate_data_transformation()
        logging.info("data transformation completed")
        print(data_tranformation_artifact)

        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config, data_tranformation_artifact)
        logging.info("initiate model trainer")
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logging.info("model trainer completed")

    except Exception as e:
        raise NetworkSecurityException(e, sys)


