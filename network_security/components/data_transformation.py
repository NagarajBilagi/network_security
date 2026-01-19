from network_security.entity.config_entity import DataTransformationConfig, TrainingPipelineConfig
from network_security.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.utils.main_utils.utils import save_numpy_array, save_object

import os, sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constant.training_pipeline import TARGET_COLUMN
from network_security.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

class DataTranformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig ):

        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            NetworkSecurityException(e, sys)

    def get_data_transformer_object(cls)-> Pipeline:
        """
        it initializes KNN imputer object with paramters defeined training_pipeline.py file and 
        returns a pipeline object with KNN imputer object
        
        cls:  DataTransformation
        """
        try:
            logging.info("initializing data transformer object that returns pipeline object")
            imputer  = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"initiating knn imputer with : {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def inintiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            train_df = DataTranformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df  = DataTranformation.read_data(self.data_validation_artifact.valid_train_file_path)

            #train dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis= 1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df =target_feature_train_df.replace(-1, 0)
            
            #test dataframe
            input_feature_test_df = test_df.drop(columns= [TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr =np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array(self.data_transformation_config.data_transformed_train_file_path, array= train_arr)
            save_numpy_array(self.data_transformation_config.data_transformed_test_file_path, array= test_arr)
            save_object(self.data_transformation_config.data_transformed_object_file_path, preprocessor_object)

            save_object("final_model/preprocessor.pkl", preprocessor_object)

            data_transformation_artifacts =DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.data_transformed_object_file_path,
                transformed_trained_file_path= self.data_transformation_config.data_transformed_train_file_path,
                transformed_test_file_path= self.data_transformation_config.data_transformed_test_file_path,
                                                                      )

            return data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e, sys)

