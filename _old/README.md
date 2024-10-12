[![Build Status](https://ci.moonstar-x.dev/job/github-webpeptide/job/python-rest-api/job/master/badge/icon)](https://ci.moonstar-x.dev/job/github-webpeptide/job/python-rest-api/job/master/)

# python-rest-api

Python REST API made with Flask. This API will handle private requests inside the application to make use of Python's
rich library set.

## Development

### Developing Under Linux

If you're running Linux, developing this project should be as simple as:

Creating a `venv`:

```text
python3 -m venv ./venv
```

Activating your `venv`:

```text
source ./venv/bin/activate
```

And then installing the dependencies:

```text
pip install -r requirements.txt
```

Finally, you can start the development server with:

```text
python3 main.py
```

This will start a development server on port 5000 accessible at http://localhost:5000

You should have the neo4j database running on your machine. You may use the [docker-compose.yml](https://github.com/WebPeptide/web-frontend/blob/master/dev/docker-compose.yml)
file from the [web-frontend](https://github.com/WebPeptide/web-frontend) repo.

You will need a `.env` file to be present in your project root. You should ask one of the developers for a copy of
this file as it is not tracked by git.

#### Native Dependencies

This project includes some native binaries that need to be installed on your machine.

First, pick a place where to save these binaries. You can use a folder inside this project directory as long as it
is not tracked by git.

Let's say you want to use the folder `/opt/bin`.

Run the following commands to acquire the native dependencies:

```text
cd /opt/bin
wget https://drive5.com/downloads/usearch11.0.667_i86linux32.gz
gzip -d usearch11.0.667_i86linux32.gz && chmod +x usearch11.0.667_i86linux32
```

### Developing Under Anything Else

The reason why developing under anything else other than Linux is that one of the native dependencies that this project
relies on will only reliably work on Linux or Windows. However, this binary does not work on any version of macOS later
than Big Sur because this binary is 32-bit.

The only way to circumvent this limitation is to use Docker as a remote development platform. You can easily achieve this
in something like [PyCharm](https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html). For any
other IDE you should research yourself how to code remotely on a Docker container.

In PyCharm, click on **Preferences > Project: Project-Name** and then click on the **Add Interpreter** button. In the dropdown,
select **On Docker**. Select `Dockerfile.dev` as the Dockerfile for the interpreter and under optional add the following as
the image tag: `webpep-dev/python-rest-api`. Click next, wait for the build stage to end and then click next again and select
the default **System Interpreter** that shows up.

Finally, inside the run configurations, you can add the `main.py` file as a run configuration. Make sure to change the
**Docker container settings** to publish the `5000` port.

#### Installing Dependencies

If you need to install a dependency, attach a terminal into a running development container and run the `pip` commands inside.
When running `pip freeze > requirements.txt` the `requirements.txt` file inside the project should be updated as long as the
container was started from PyCharm since it automatically creates the relevant volumes.

Restarting the development container will re-build the image and add the new dependency. The caveat of this process is that
the development image may re-download all the dependencies (including already installed ones).

## Building

You can build this application to generate a Docker image.

To do so, run the following command:

```text
docker build -t webpep/python-rest-api .
```

This will create a `webpep/python-rest-api` Docker image in your local machine.
