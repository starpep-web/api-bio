from fastapi import FastAPI
from pkg.handlers import router, load_controllers
from pkg.middleware.handlers import register_error_handler


def create_app():
    app = FastAPI()

    load_controllers()
    app.include_router(router, prefix="")
    register_error_handler(app)

    return app


fastapi_app = create_app()
