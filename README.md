# Project Gdansk

## Docker

* `docker build -t pgdansk .`
* `docker run --rm -v "$(pwd)/app:/app/app" pgdansk`
* `docker run -ti --rm -v "$(pwd)/app:/app/app" -e PYTHONPATH=/app pgdansk python tests/tests.py`
* `docker run -ti --rm -v "$(pwd)/app:/app/app" -e PYTHONPATH=/app pgdansk python -m unittest discover -v`
* `docker run -ti --rm -v "$(pwd)/app:/app/app" pgdansk green`
* `docker run -ti --rm -v "$(pwd)/app:/app/app" pgdansk green -vv`
* `docker run -ti --rm -v "$(pwd)/app:/app/app" -v "$(pwd)/test_data:/test_data" pgdansk`
