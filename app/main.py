from fastapi import FastAPI
import sqlalchemy

from config import Config as config
from app.database.database import database, metadata


def setup_database(app):
    app.state.database = database

    @app.on_event("startup")
    async def startup():
        engine = sqlalchemy.create_engine(config.SQLALCHEMY_DATABASE_URI)
        metadata.create_all(engine)

        database_ = app.state.database
        if not database_.is_connected:
            await database_.connect()

    @app.on_event("shutdown")
    async def shutdown():
        database_ = app.state.database
        if database_.is_connected:
            await database_.disconnect()


def create_app():
    app = FastAPI()
    setup_database(app)

    from app.movies.routers import movie_router
    from app.auth.routers import auth_router

    app.include_router(movie_router)
    app.include_router(auth_router)

    @app.get("/")
    def index():
        return {"message": "Hello, World!"}

    return app
