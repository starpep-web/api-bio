FROM python:3.8

WORKDIR /opt/bin

RUN wget https://drive5.com/downloads/usearch11.0.667_i86linux32.gz
RUN gzip -d usearch11.0.667_i86linux32.gz && chmod +x usearch11.0.667_i86linux32

WORKDIR /opt/app

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install waitress

COPY . .

ENV BIN_LOCATION /opt/bin
ENV ASSETS_LOCATION /opt/files
ENV TEMP_ARTIFACTS_LOCATION /tmp/files

EXPOSE 8080

CMD ["waitress-serve", "--call", "main:create_app"]
