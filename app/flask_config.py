from flask import Flask
from flask_restful import Api
from flask_pymongo import pymongo
from utils.helpers import check_file_existance, get_configs

import os
import logging

app = Flask(__name__)
api = Api(app)
db = None
orders_collection = None

APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT")


def main_config():
    MONGODB_URI = os.getenv("MONGODB_URI")
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_database('orders_service')
    orders_collection = pymongo.collection.Collection(db, 'orders')
    print("Connected to db!")

def development_config():
    # read db_config
    from configparser import RawConfigParser, NoSectionError
    # check if db_config ini exists
    check_file_existance("app/db_config.ini")

    config = RawConfigParser()
    config.optionxform = str

    config.read("app/db_config.ini")

    try:
        config_dict = get_configs(config=config, section="ENVIRONMENT")
    except NoSectionError:
        logging.error(
            "Error occured in db_config.ini file. Check for mistypes!")
        os._exit(0)

    os.environ = config_dict


if APP_ENVIRONMENT == "development":
    development_config()

    main_config()

elif APP_ENVIRONMENT == "production":
    main_config()
