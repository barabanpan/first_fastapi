# My first FastAPI project

## Prerequisites
1. ```pip install -r requirements.txt```

2. In root directory create file `config.py`:
```
import os
import datetime

sqlite_uri = os.path.abspath("app/database/database.db")


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '{secred-key-here}'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sqlite_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
```

## Run
```uvicorn run:app --reload```

Urls like [127.0.0.1:8000/docs](127.0.0.1:8000/docs) and [127.0.0.1:8000/redoc](127.0.0.1:8000/redoc) will open documentation.