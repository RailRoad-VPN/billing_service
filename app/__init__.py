import logging
from pprint import pprint

from flask import Flask

from app.common.psql_helper import PostgreSQL
from app.common.storage import DBStorageService
from app.resources.user import UserAPI

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Load the default configuration
app.config.from_object('config.DevelopmentConfig')

with app.app_context():
    psql = PostgreSQL(app=app)

db_storage_service = DBStorageService(psql=psql)

# USER API
user_api_url = '%s/%s' % (app.config['API_BASE_URI'], UserAPI.__api_url__)
user_api_view_func = UserAPI.as_view('user_api', db_storage_service)
app.add_url_rule(user_api_url, view_func=user_api_view_func, methods=['GET', 'POST', ])
app.add_url_rule('%s/uuid/<string:uuid>' % user_api_url, view_func=user_api_view_func, methods=['GET', 'PUT'])
app.add_url_rule('%s/email/<string:email>' % user_api_url, view_func=user_api_view_func, methods=['GET'])

pprint(app.url_map._rules_by_endpoint)
