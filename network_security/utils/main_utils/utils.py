import yaml
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException


import os, sys
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path)-> dict:
    try:
        with open(file_path, mode= 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path:str, content: object, replace:bool = False )-> None:

    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok= True)
        with open(file_path,'w') as file:
            yaml.dump(content, file)

    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_numpy_array(file_path: str, array:np.array):
    """
    save numpy array to a file
    
    :param=> file_path: location to save a file
    :param=> array: np.array to save
    """
    try:

        dir_path =os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        with open(file_path, "wb") as file_object:
            np.save(file_object, array)

    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_object(file_path : str, obj: object):
    try:
        logging.info("entered save_object method of main_utils class")
        dir_path =os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        with open(file_path , "wb") as file_object:
            pickle.dump(obj, file_object)
        logging.info("exited save_object method of main_utils class")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_object(file_path: str)-> object:

    try:
        if not os.path.exists(file_path):
            raise Exception(f"{file_path} does not exists")

        with open(file_path, "rb") as obj:
            return pickle.load(obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array_data(file_path: str)-> np.array:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"{file_path} does not exists")
              
        with open(file_path, 'rb') as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def evaluate_models(x_train, y_train, x_test, y_test, models, parameters)-> dict:
    try:
        report=  {}

        for i in range (len(list(models))):
            model = list(models.values())[i]
            para = parameters[list(models.keys())[i]]

            gs = GridSearchCV(model,para, cv = 3)
            gs.fit(x_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_true= y_train, y_pred=y_train_pred)
            print('train_model_score :', train_model_score)
            test_model_score = r2_score(y_true= y_test, y_pred=y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e,sys)
