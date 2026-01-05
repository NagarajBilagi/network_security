import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

mongo_db_url= os.getenv('MONGO_DB_URL')
print(mongo_db_url)

import pandas as pd
import pymongo
import numpy as np
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException (e, sys)
        

    def csv_to_json_coverter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop= True, inplace= True)
            records = list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, collection, databse):
        try:
            self.records = records
            self.collection = collection
            self.database = databse

            self.mongo_client= pymongo.MongoClient(mongo_db_url)
            self.database= self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ =='__main__':
    FILE_PATH = "C:\\Users\\nagar\\Desktop\\projects\\AI_projects\\Network_Security\\Network_Data\\phisingData.csv"
    DATABASE = "NagarajAI"
    Collection = "NetworkData"
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_coverter(file_path= FILE_PATH)
    no_of_records = network_obj.insert_data_to_mongodb(records, Collection, DATABASE)
    print(no_of_records)