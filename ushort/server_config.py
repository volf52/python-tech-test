import multiprocessing

from gunicorn.app.base import BaseApplication
from uvicorn import Config, Server

from ushort.logging import StubbedGunicornLogger


class GunicornApp(BaseApplication):
    def __init__(self, app, opts=None):
        self.opts = opts or {}
        self.app = app
        super(GunicornApp, self).__init__()

    def load_config(self):
        config = {
            k: v
            for k, v in self.opts.items()
            if k in self.cfg.settings and v is not None
        }

        for k, v in config.items():
            self.cfg.set(k.lower(), v)

    def load(self):
        return self.app


def create_gunicorn_server(base_app, *, port: int, workers: int = None):
    options = {
        "bind": f"0.0.0.0:{port}",
        "workers": workers or (multiprocessing.cpu_count() + 1) // 2,
        "accesslog": "_",
        "errorlog": "_",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "logger_class": StubbedGunicornLogger,
    }

    return GunicornApp(base_app, options)


def create_uvicorn_server(base_app, *, port: int, log_level: str):
    server = Server(Config(base_app, host="0.0.0.0", log_level=log_level, port=port))

    return server
