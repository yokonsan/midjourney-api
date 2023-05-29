import uvicorn
from fastapi import FastAPI

import settings_server  # noqa
from src.core.server.handlers import exc_handler
from src.core.server.routers import root_router


def init_app():
    app = FastAPI(title="Midjourney API")
    
    app.include_router(root_router, prefix=settings_server.API_PREFIX)
    exc_handler(app)
    
    return app


def run(host, port):
    app = init_app()
    uvicorn.run(app, port=port, host=host)


if __name__ == '__main__':
    run("0.0.0.0", 8062)
