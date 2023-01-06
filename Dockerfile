FROM python:3.8

WORKDIR /opt/app

RUN pip install pipenv

COPY Pipfile* ./
RUN pipenv sync --system
RUN pip install waitress

COPY . .

EXPOSE 8080

CMD ["waitress-serve", "--call", "main:create_app"]
