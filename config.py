class Config(object):
    DEBUG = False
    TESTING = False

    APP_SESSION_SK = 'TPrvrXj9bPdPSMrPyKs'
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = APP_SESSION_SK
    TEMPLATES_AUTO_RELOAD = True

    VERSION = 'v1'
    API_BASE_URI = '/api/%s' % VERSION


class ProductionConfig(Config):
    ENV = 'production'
    LOG_PATH = ''

    PSQL_DBNAME = 'rrnbilling'
    PSQL_USER = 'railroadman'
    PSQL_PASSWORD = ''
    PSQL_HOST = '127.0.0.1'


class DevelopmentConfig(Config):
    ENV = 'development'
    LOG_PATH = '/Users/dikkini/Developing/workspaces/my/DFN/logs/billing'

    DEBUG = True

    PSQL_DBNAME = 'rrnbilling'
    PSQL_USER = 'railroadman'
    PSQL_PASSWORD = 'railroadman'
    PSQL_HOST = '127.0.0.1'


class TestingConfig(Config):
    TESTING = True
    ENV = 'testing'
    LOG_PATH = '/opt/apps/dfn/logs/billing'

