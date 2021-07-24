import os
import datetime
from stralette.config import Config


sqlite_uri = os.path.abspath("app/database/database.db")
config = Config(".env")


class Config(object):
    DEBUG = config("DEBUG", default=True)
    DEVELOPMENT = config("DEVELOPMENT", default=True)
    TESTING = config("TESTING", default=True)
    CSRF_ENABLED = True  # ?
    SECRET_KEY = config("SECRET_KEY", default="#saf@$324#%^TEr")

    PERMANENT = True  # session lives after browser restart
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=2)

    JWT_SECRET_KEY = config("JWT_SECRET_KEY", default="$#3254%$^sgfefwE")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlite_uri
