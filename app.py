from fastapi import FastAPI
from dotenv import load_dotenv
import os, sys
import certifi

import pymongo
import pandas as pd

from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException

from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.utils.main_utils.utils import load_object, save_object, load_numpy_array_data

from network_security.constant.training_pipeline import (DATA_INGESTION_COLLECTION_NAME, 
                                                         DATA_INGESTION_DATABASE_NAME)


from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse


ca =certifi.where()
load_dotenv()
MONGODBURL = os.getenv('MONGO_DB_URL')


client = pymongo.MongoClient(MONGODBURL)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(CORSMiddleware, 
                   allow_origins= origins, 
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"])

@app.get(path= "/", tags=["authentication"])
async def index():
    return RedirectResponse(url= "/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("training is successfull")
    except Exception as e:
        raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    app_run(app= app, host= "localhost", port= 8000)



