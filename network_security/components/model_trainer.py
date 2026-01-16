from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException

from network_security.entity.config_entity import ModelTrainerConfig
from network_security.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from network_security.constant import training_pipeline

from network_security.utils.main_utils.utils import save_object, load_object
from network_security.utils.main_utils.utils import load_numpy_array_data, evaluate_models
from network_security.utils.ml_utils.model.estimator import NewtworkModel
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score

import os, sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier)

class ModelTrainer:
    def __init__(self, model_trainer_config :ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact


    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            
            models = {
                'Random Forest' : RandomForestClassifier(verbose=1),
                'Decision Tree' : DecisionTreeClassifier(),
                'Gradient Boosting' : GradientBoostingClassifier(verbose=1),
                'Logistic Regression' : LogisticRegression(verbose= 1),
                'Adaboost' : AdaBoostClassifier()
            }

            params = {
                'Decision Tree' :{
                'criterion' : ['gini', 'entropy', 'log_loss']
            },

            "Random Forest" :{
                'n_estimators' : [8, 16, 32, 64, 128, 256]
            },

            "Gradient Boosting" : {
                'learning_rate' : [.1, .01, 0.5, 0.001],
                'n_estimators' : [8, 16, 32, 64, 128, 256]
            },

            "Logistic Regression" : {},
            "Adaboost" : {
                'learning_rate' : [0.1, 0.01, 0.5, 0.001],
                'n_estimators'  : [8, 16, 32, 64, 128, 256]
            }
            
            }

            model_report: dict = evaluate_models(x_train, y_train, x_test, y_test, models= models, parameters= params)
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]
            y_train_pred = best_model.predict(x_train)

            classification_train_metric= get_classification_score(y_train_pred, y_train)

            # track mlfow
            y_test_pred =best_model.predict(x_test)
            classification_test_metric = get_classification_score(y_test_pred, y_test)

            preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok= True)

            network_model= NewtworkModel(preprocessor,model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path, obj= NewtworkModel)

            # model trainer artifact
            model_trainer_artifact =ModelTrainerArtifact(trained_model_file_path= self.model_trainer_config.trained_model_file_path,
                                                         train_metric_artifact= classification_train_metric,
                                                         test_metric_artifact= classification_test_metric)
            
            logging.info(f"model trainer artifact {model_trainer_artifact}")

            return model_trainer_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_model_trainer(self)-> ModelTrainerArtifact:
        try:

            train_file_path = self.data_transformation_artifact.transformed_trained_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path


            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            print('train_arr_shape ', train_arr.shape)
            print('test_arr_shape ', test_arr.shape)

            x_train, y_train, x_test, y_test  = (
                train_arr[:, :-1], 
                train_arr[:, -1], 
                test_arr[:, :-1], 
                test_arr[:, -1])
            # print('x_train :', x_train.shape)
            # print('y_train :', y_train.shape)
            # print('x_test :', x_test.shape)
            # print('y_test :', y_test.shape)
            # print('before_function')
            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)