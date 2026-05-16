import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import numpy as np
import pymongo
from pymongo.server_api import ServerApi
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

# Trusted certificate authority
ca = certifi.where()

class DataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = data.to_dict(orient='records')
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def load_data_mongodb(self, records, db, collection):
        try:
            self.db = db
            self.collection = collection
            self.records = records

            self.mongoClient = pymongo.MongoClient(MONGODB_URI, server_api=ServerApi('1'))
            self.db =  self.mongoClient[self.db]
            self.collection = self.db[self.collection]

            self.collection.insert_many(self.records)
            return f"{len(self.records)} records loaded successfully in MONGO DB"
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "network_data/phisingData.csv"
    DATABASE = "NETWORK_SECURITY_DB"
    COLLECTION = "NETWORK_COLLECTION"

    network_obj = DataExtract()

    # Convert CSV to json
    records = network_obj.csv_to_json(FILE_PATH)
    records_count = network_obj.load_data_mongodb(records=records,db=DATABASE, collection=COLLECTION)

    print(records_count)

