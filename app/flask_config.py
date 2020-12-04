from flask import Flask
from flask_restful import Api
from flask_mongoengine import MongoEngine
from utils.helpers import check_file_existance, get_configs

import os
import logging

logging.getLogger().setLevel(logging.INFO)
app = Flask(__name__)
api = Api(app)

db = None

APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT")


def main_config(configs):
    app.config['MONGODB_SETTINGS'] = {
        'db': configs["MONGODB_DB"],
        'host': configs['MONGODB_HOST'],
    }
    db = MongoEngine()

    db.init_app(app)
    print("Connected to db!")

    return db


def development_config():
    # read db_config
    from configparser import RawConfigParser, NoSectionError
    # check if db_config ini exists
    check_file_existance("app/db_config.ini")

    config = RawConfigParser()
    config.optionxform = str

    config.read("app/db_config.ini")

    try:
        config_db_dict = get_configs(config=config, section="DATABASE")
    except NoSectionError:
        logging.error(
            "Error occured in db_config.ini file. Check for mistypes!")
        os._exit(0)

    return config_db_dict


def production_config():
    return os.environ

if APP_ENVIRONMENT == "development":
    configs = development_config()

    db = main_config(configs=configs)

elif APP_ENVIRONMENT == "production":
    configs = production_config()

    db = main_config(configs=configs)
