from fastapi import FastAPI


def create_app():
    app = FastAPI()

    @app.get("/")
    def index():
        return {"message": "Hello, World!"}

    return app
