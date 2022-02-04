import ormar
from typing import List, Optional

from app.database.database import metadata, database


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
    title: str = ormar.String(max_length=120)
    plot: str = ormar.String(max_length=1000)
    year: int = ormar.Integer()
    genres: Optional[List[Genre]] = ormar.ManyToMany(Genre)


class Like(ormar.Model):
    class Meta:
        tablename = "movies_x_users"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    rate: float = ormar.Float()
