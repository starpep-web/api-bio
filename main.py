from fastapi import FastAPI
from pkg.handlers import router, load_controllers


def create_app():
    app = FastAPI()

    load_controllers()
    app.include_router(router, prefix="")

    return app


fastapi_app = create_app()
