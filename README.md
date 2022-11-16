# My first FastAPI project

Movie data taken from [here](https://www.kaggle.com/rounakbanik/the-movies-dataset?select=movies_metadata.csv).

## Prerequisites
1. ```pip install -r requirements.txt```

2. ```alembic upgrate head```

3. ```python load_to_database.py```

## Run
```uvicorn run:app --reload```

Urls like [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and [127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) will open documentation.

## TODO:

1. add table LikedMovies(user_id, movie_id, rate) and CRUD for it
2. password reset and change
3. login part 
4. refresh token 
5. /me to return user profile
6. /get-recommendations based on liked movies
7. search by movie's title or discription 
8. improve search by description using nlp
