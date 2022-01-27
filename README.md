# My first FastAPI project

Movie data taken from [here](https://www.kaggle.com/rounakbanik/the-movies-dataset?select=movies_metadata.csv).

## Prerequisites
1. ```pip install -r requirements.txt```

2. ```alembic upgrate head```

3. ```python load_to_database.py```

## Run
```uvicorn run:app --reload```

Urls like [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and [127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) will open documentation.
