from ushort.app import app
from ushort.logging import configure_logger_for_gunicorn

configure_logger_for_gunicorn()

if __name__ == "__main__":
    import os

    from ushort.server_config import create_gunicorn_server

    workers = int(os.environ.get("WORKERS", 4))

    gunicorn_server = create_gunicorn_server(app, port=8013, workers=workers)

    gunicorn_server.run()
