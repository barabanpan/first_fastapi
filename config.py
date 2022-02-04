import os
from starlette.config import Config


sqlite_uri = os.path.abspath("app/database/database.db")
config = Config(".env")


class Config(object):
    DEBUG = config("DEBUG", default=True)
    DEVELOPMENT = config("DEVELOPMENT", default=True)
    TESTING = config("TESTING", default=True)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlite_uri
    SECRET_KEY = config("SECRET_KEY", default="wef#$SEFCE123ED$REWeEWRsdf3$@@")
    ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=10080)
    HASHING_ALGORITHM = config("HASHING_ALGORITHM", default="HS256")
