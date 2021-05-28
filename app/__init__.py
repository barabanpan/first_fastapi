from fastapi import FastAPI

from .routers.employee import employee_router


def create_app():
    app = FastAPI()
    app.include_router(employee_router)

    @app.get("/")
    def index():
        return {"message": "Hello, World!"}

    return app
