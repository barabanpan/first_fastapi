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

1. і юзерських вподобань LikedMovies(user_id, movie_id, rate) щоб можна було додавати і видаляти собі їх, і редагувати, 
2. круд
3. зміну пароля, 
4. логін, 
5. рефрештокен і 
6. окремо мі по токену
7. гет рекомендейшнс, якщо нема лайкнутих мувіз, то сказати про це
8. пошук фільм по опису, тіпа пост, що повертає фільм

