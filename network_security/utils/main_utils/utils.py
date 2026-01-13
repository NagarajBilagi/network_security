import yaml
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException


import os, sys
import numpy as np
import pickle

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

