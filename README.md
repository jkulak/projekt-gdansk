# Project Gdansk

## Docker

* `docker build -t pgdansk .`
* `docker run -ti --rm -v "$(pwd)/src:/app/src" -v "$(pwd)/test_data:/app/test_data" pgdansk`
* `docker run -ti --rm -v "$(pwd)/src:/app/src" -v "$(pwd)/tests:/app/tests" pgdansk green -vv`
