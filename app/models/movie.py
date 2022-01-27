import ormar
from typing import List, Optional

from .database import metadata, database


class Genre(ormar.Model):
    class Meta:
        tablename = "genres"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)


class Movie(ormar.Model):
    class Meta:
        tablename = "movies"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=100)
    plot: str = ormar.String(max_length=2000)
    year: int = ormar.Integer()
    genres: Optional[List[Genre]] = ormar.ManyToMany(Genre)
