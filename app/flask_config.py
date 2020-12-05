import logging
import os

from flask import Flask
from flask_restful import Api
from mongoengine import connect

from utils.helpers import check_file_existance, get_configs

logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

db = None

APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT")


def main_config(configs):
    db_host = f"{configs['MONGODB_HOST']}:{configs['MONGODB_PORT']}"

    client = connect(
        'orders_service',
        host=db_host,
        port=int(configs['MONGODB_PORT'])
    )

    db = client['orders_service']

    # client.orders_service.command("ping")

    if client.orders_service.command("ping") == {u'ok': 1.0}:
        logger.info("Connected to db!")

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
