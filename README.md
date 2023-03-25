# Project Gdansk

## Docker

* `docker build -t pgdansk .`
* `docker run --rm -v "$(pwd)/app:/app/app" -v "$(pwd)/tests:/app/tests" pgdansk`
* `docker run -ti --rm -v "$(pwd)/app:/app/app" -v "$(pwd)/tests:/app/tests" -e PYTHONPATH=/app pgdansk python tests/tests.py`
* `docker run -ti --rm -v "$(pwd)/app:/app/app" -v "$(pwd)/tests:/app/tests" -e PYTHONPATH=/app pgdansk python -m unittest discover -v`
* `docker run -ti --rm -v "$(pwd)/app:/app/app" -v "$(pwd)/tests:/app/tests" pgdansk green`
* `docker run -ti --rm -v "$(pwd)/app:/app/app" -v "$(pwd)/tests:/app/tests" pgdansk green -vv`
