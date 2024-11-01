# API - Bio

This repository contains the code for the API service that communicates to the Database and exposes endpoints to interact with it alongside Bio specific alignment algorithms and search export functionality.

No endpoint documentation is available yet since this API is not meant to be used publicly.

## Requirements

In order to develop for this repository you need:

* [Python 3.12](https://www.python.org) (but any `>3.12` should work fine)
* [Docker](https://www.docker.com/products/docker-desktop/)
* Have [env-development](https://github.com/starpep-web/env-development) running locally.

## Development

First, clone this repository:

```bash
git clone https://github.com/starpep-web/api-bio
```

Create an environment:

```bash
python3 -m venv ./venv
```

Load the environment:

```bash
source ./venv/bin/activate
```

(Or, if you're on Windows, you might have to do it with:)

```powershell
.\env\Scripts\activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create an `.env` file with the following contents:

```text
REDIS_URI=redis://localhost:6379
NEO4J_DB_URI=bolt://localhost:7687
ASSETS_LOCATION=/path/to/files
TEMP_ARTIFACTS_LOCATION=/path/to/artifacts
```

Run the `fastapi` entrypoint:

```bash
fastapi dev main.py
```

And done, the service should be reachable at `http://localhost:8000`.

## Testing

Some testing commands are available to you:

### `pytest test`

This command will run unit tests once.

### `ptw test`

This command will run the unit test runner in watch-mode.

## Building

If you're developing this on your local machine, consider building the Docker image with the following command:

```bash
docker build -t local-starpep/api-bio:latest .
```

You can create a new container to try it out with the following command:

```bash
docker run -it --rm -p 8000:8000 -e REDIS_URI=redis://localhost:6379 -e NEO4J_DB_URI=bolt://localhost:7687 -e ASSETS_LOCATION=/path/to/files -e TEMP_ARTIFACTS_LOCATION=/path/to/artifacts local-starpep/api-bio:latest
```

And done, the service should be reachable at `http://localhost:8000`.

## Production

Consider checking this [docker-compose.yml](https://github.com/starpep-web/env-production/blob/main/docker-compose.yml) for an example on how to run this image in production.
