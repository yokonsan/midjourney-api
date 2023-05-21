import __init__  # noqa
from app import server

api_app = server.init_app()


if __name__ == '__main__':
    server.run("0.0.0.0", 8062)
