from fastapi import FastAPI

from config import DevelopmentConfig as config
from .models.database import db, base


def setup_database(app):
    @app.on_event("startup")
    def create_tables():
        base.metadata.create_all(db)


def create_app():
    app = FastAPI()
    setup_database(app)

    from .routers.employee import employee_router
    app.include_router(employee_router)

    @app.get("/")
    def index():
        return {"message": "Hello, World!"}

    return app
