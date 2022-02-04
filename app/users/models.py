import ormar
from typing import List, Optional

from app.database.database import metadata, database
from app.movies.models import Movie, Like


class User(ormar.Model):
    class Meta:
        tablename = "users"
        metadata = metadata
        database = database

    id: str = ormar.String(primary_key=True, max_length=50)
    email: str = ormar.String(max_length=50, unique=True)
    hashed_password: str = ormar.String(max_length=100)
    is_active: bool = ormar.Boolean(default=True)
    is_admin: bool = ormar.Boolean(default=False)
    joined: int = ormar.Integer()  # timestamp
    liked_movies: Optional[List[Movie]] = ormar.ManyToMany(Movie, through=Like)
