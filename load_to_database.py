import os
import json

import pandas as pd

from config import Config as config
from app.models.movie import Movie, Genre



def clean_data(m):
    # Remove columns we don't need
    columns_to_drop = ["adult", "belongs_to_collection", "budget", "homepage", "id", "imdb_id", "original_language",
        "popularity", "poster_path", "production_companies", "production_countries", "revenue", "runtime",
        "spoken_languages", "tagline", "video", "vote_average", "vote_count"]
    m = m.drop(columns_to_drop, axis=1)

    # Only leave released movies
    m = m[m.status == "Released"]

    # Get only years from release date
    m["year"] = m.release_date.apply(lambda d: str(d)[0:4] if not pd.isna(d) else pd.np.NAN) # 
    m = m.drop(["release_date"], axis=1)
    m = m.sort_values("year", ascending=False)

    # Remove movies without genres
    m = m[m.genres != "[]"]

    # Write genres in different form
    genres_list = []

    def to_list(gs):
        sub = []
        gs = gs.replace("'", '"')
        gs = json.loads(gs)
        for dct in gs:
            genres_list.append(dct["name"])
            sub.append(dct["name"])
        return sub

    m.genres = m.genres.apply(to_list)

    genres_set = set(genres_list)

    # Remove movies, released before 1950
    def to_int_or_def(y, def_):
        try:
            return int(y)
        except:
            return def_

    m = m[m.year.apply(lambda x: to_int_or_def(x, 2017)) >= 1950]
    m["year"] = m.year.apply(lambda x: to_int_or_def(x, 0))

    return m, genres_set


def write_genres(genres):
    genres_with_id = []
    for name in genres:
        g = Genre.objects.create(name=name)
        genres_with_id.append(g)
    return genres_with_id


def write_movies(movies, genres_with_id):

    def create_one(title, plot, year, genres):
        m = Movie(title=title, plot=str(plot), year=year)
        for genre in genres_with_id:
            if genre in genres:
                m.genres.add(genre)

    movies.apply(lambda m: create_one(m["title"], m["overview"], m["year"], m["genres"]), axis=1)


if __name__ == "__main__":
    m = pd.read_csv("movies_csv/movies_metadata.csv")
    movies, genres = clean_data(m)

    genres_with_id = write_genres(genres)
    write_movies(movies, genres_with_id)
