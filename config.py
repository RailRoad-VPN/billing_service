class Config(object):
    DEBUG = False
    TESTING = False

    APP_SESSION_SK = 'TPrvrXj9bPdPSMrPyKs'
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = APP_SESSION_SK
    TEMPLATES_AUTO_RELOAD = True

    VERSION = '1.0'
    API_BASE_URI = '/api/%s' % VERSION


class ProductionConfig(Config):
    PSQL_DBNAME = ''
    PSQL_USER = ''
    PSQL_PASSWORD = ''
    PSQL_HOST = ''


class DevelopmentConfig(Config):
    DEBUG = True

    PSQL_DBNAME = ''
    PSQL_USER = ''
    PSQL_PASSWORD = ''
    PSQL_HOST = ''


class TestingConfig(Config):
    TESTING = True
