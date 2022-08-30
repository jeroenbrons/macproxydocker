FROM python:3.9

WORKDIR /usr/src/app
COPY . .
RUN pip3 install  --no-cache-dir  -r requirements.txt
COPY Docker /usr/bin
RUN chmod +x /usr/bin/start.sh
EXPOSE 5000
ENTRYPOINT [ "start.sh" ]
