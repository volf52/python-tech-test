# URL Shortener - Tech Test

## Wanna run it on your computer???

You have two choicesfor creating the virtual env and installing the packages.
You can either use the awesome tool [Poetry](https://python-poetry.org/), or you can use the old ways and create a venv using `python -m venv [path to the desired venv location]`.

#### Poetry (recommended, especially if you want to contribute to this repo)

If you went the poetry route, you can create the virtualenv and install the requirements in one go by running `poetry install` inside the repo dir.
After that, run `poetry shell` inside the dir whenever you want to activate the environment, and have fun.

#### Venv

For updating your paths etc to use the venv, you have to run `source [path to venv]/bin/activate`. 
If you are developing on Windows (for some reason), replace `bin` with `Scripts`.

Ensure the virtual env is active using `which python` (or `where python` / `whereis python`).
Then run `python -m pip install -r requirments.txt` from the repo dir to install all the requirements.

---

## Running the application

---

Once the application is past the start-up phase, you can send the API requests to it.
By default, the server will run on port 8013, but you can change this by either setting the PORT environment variable, or through the *_app.py files directly.
The details for the API routes, and the parameters they expect, can be viewed at `https://localhost:8013/docs` and `https://localhost:8013/redoc`.

### Simple Uvicorn

You can launch it either using `[poetry run] python uvicorn_app.py` or simply `[poetry run] uvicorn uvicorn_app:app --port $PORT`.

### Gunicorn

The commands are similar to uvicorn. The added thing is that multiple workers run, helping us scale the application to server more users.
The number of workers in the first command can be controlled either through the `gunicorn_app.py` file directly, or through the `WORKERS` env variable.

- `[poetry run] python gunicorn_app.py`
- `[poetry run] gunicorn -b :$PORT --threads 8 -w 2 -k uvicorn.workers.UvicornWorker gunicorn_app:app`. Here, `-w` specifies the number of workers.
