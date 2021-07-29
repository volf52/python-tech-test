from ushort.app import app
from ushort.logging import configure_logger_for_uvicorn

configure_logger_for_uvicorn()

if __name__ == "__main__":
    import logging

    from ushort.server_config import create_uvicorn_server

    log_level = logging.getLevelName("INFO")

    uvicorn_server = create_uvicorn_server(app, port=8013, log_level=log_level)

    uvicorn_server.run()
