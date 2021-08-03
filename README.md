# My first FastAPI project

## Prerequisites
1. ```pip install -r requirements.txt```

2. In root directory create file `.env`:
```
DEBUG=true
DEVELOPMENT=true
TESTING=true
SECRET_KEY={your-secret-key}
JWT_SECRET_KEY={your-jwt-secret-key}
```

## Run
```uvicorn run:app --reload```

Urls like [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and [127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) will open documentation.
