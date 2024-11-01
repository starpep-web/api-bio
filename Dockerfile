FROM python:3.12-alpine

RUN apk add --update --no-cache gcc libc-dev

RUN adduser -D starpep-api-bio
WORKDIR /opt/app

ENV ASSETS_LOCATION=/opt/files
ENV TEMP_ARTIFACTS_LOCATION=/tmp/files

COPY --chown=starpep-api-bio requirements.txt ./
RUN pip install -r requirements.txt

COPY --chown=starpep-api-bio . .

EXPOSE 8000

USER starpep-api-bio
CMD ["fastapi", "run", "main.py", "--port", "8000", "--proxy-headers"]
