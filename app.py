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

from network_security.utils.ml_utils.model.estimator import NewtworkModel


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

from fastapi.templating import Jinja2Templates
templates= Jinja2Templates(directory= "./templates")

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

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        network_model =NewtworkModel(preprocessor= preprocessor, model= model)
        print(df.iloc[0])
        y_pred =network_model.predict(df)
        print('y_pred :',y_pred)
        df['predicted_column'] = y_pred
        print(df["predicted_column"])
        df.to_csv("prediction_output/output.csv")
        table_html = df.to_html(classes= "table table-striped")
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
if __name__ == "__main__":  
    app_run(app= app, host= "0.0.0.0", port= 8000)



