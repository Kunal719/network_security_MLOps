import os
import sys

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

mongo_db_uri = os.getenv('MONGODB_URI')

import pymongo
from pymongo.server_api import ServerApi

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

client = pymongo.MongoClient(mongo_db_uri, server_api=ServerApi('1'))
db = client[DATA_INGESTION_DATABASE_NAME]
collection = db[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory='./templates')

@app.get("/", tags=["Authentication"])
async def index():
    RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training successful!!")
    except Exception as e:
        return NetworkSecurityException(e, sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile=File(...)):
    try:
        data = pd.read_csv(file.file)
        preprocessor = load_object(file_path="final_models/preprocessor.pkl")
        model = load_object(file_path="final_models/model.pkl")

        network_model = NetworkModel(model=model, preprocessor=preprocessor)
        y_pred = network_model.predict(data)
        
        data['prediction'] = y_pred

        data.to_csv("prediction_output/prediction.csv", index=False)

        table_data = data.to_html(classes="table table-striped table-hover table-bordered table-sm")
        return templates.TemplateResponse("table.html", {"request": request, "table": table_data})
    except Exception as e:
        return NetworkSecurityException(e, sys)

    
if __name__ == "__main__":
    app_run("app:app", host="0.0.0.0", port=8000, reload=True)