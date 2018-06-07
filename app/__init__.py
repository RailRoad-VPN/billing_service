import logging
import os
import sys

from flask import Flask

from app.resources.subscriptions import SubscriptionsAPI
from user_subscriptions import UserSubscriptionsAPI

sys.path.insert(0, '../psql_library')
from psql_helper import PostgreSQL
from storage_service import DBStorageService

sys.path.insert(1, '../rest_api_library')
from api import register_api

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load config based on env variable
ENVIRONMENT_CONFIG = os.environ.get("ENVIRONMENT_CONFIG", default='DevelopmentConfig')
logging.info("Got ENVIRONMENT_CONFIG variable: %s" % ENVIRONMENT_CONFIG)
config_name = "%s.%s" % ('config', ENVIRONMENT_CONFIG)
logging.info("Config name: %s" % config_name)
app.config.from_object(config_name)

with app.app_context():
    psql = PostgreSQL(app=app)

db_storage_service = DBStorageService(psql=psql)

app_config = app.config
api_base_uri = app_config['API_BASE_URI']

apis = [
    {'cls': SubscriptionsAPI, 'args': [db_storage_service, app_config]},
    {'cls': UserSubscriptionsAPI, 'args': [db_storage_service, app_config]},
]

register_api(app, api_base_uri, apis)
