[![Build Status](https://ci.moonstar-x.dev/job/github-webpeptide/job/python-rest-api/job/master/badge/icon)](https://ci.moonstar-x.dev/job/github-webpeptide/job/python-rest-api/job/master/)

# python-rest-api

Python REST API made with Flask. This API will handle private requests inside the application to make use of Python's
rich library set.

## Development

To start development, make sure to have `pipenv` installed:

```text
pip install pipenv
```

Once you have it installed, create a `pipenv` environment for this project:

```text
pipenv sync
```

If you're using PyCharm, you may need to run `pipenv --venv` to get the path for your virtual environment. You should
configure your Python interpreter as a `System Interpreter` with the `python3` binary taken from the environment that was
returned by the `pipenv --venv` command.

You should have the neo4j database running on your machine. You may use the [docker-compose.yml](https://github.com/WebPeptide/web-frontend/blob/master/dev/docker-compose.yml)
file from the [web-frontend](https://github.com/WebPeptide/web-frontend) repo.

### Working

To load your `pipenv` environment, run:

```text
pipenv shell
```

To start the development server, run:

```text
python3 main.py
```

This will start a development server on port 5000 accessible at http://localhost:5000

You will need a `.env` file to be present in your project root. You should ask one of the developers for a copy of
this file as it is not tracked by git.

## Building

You can build this application to generate a Docker image.

To do so, run the following command:

```text
docker build -t webpep/python-rest-api .
```

This will create a `webpep/python-rest-api` Docker image in your local machine.
