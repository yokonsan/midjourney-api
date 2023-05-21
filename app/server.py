import uvicorn
from fastapi import FastAPI


def init_app():
    _app = FastAPI(title="Midjourney API")
    register_blueprints(_app)

    return _app


def register_blueprints(open_app):
    from app import routers
    open_app.include_router(routers.router, prefix="/v1/api")


def run(host, port):
    open_app = init_app()
    uvicorn.run(open_app, port=port, host=host)
