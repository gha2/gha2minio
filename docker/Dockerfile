FROM alpine:3.11

WORKDIR /usr/app

RUN apk add --no-cache python3

COPY ./setup/requirements.txt ./

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r ./requirements.txt

COPY ./src/*.py ./src/logging.yml ./

COPY ./docker/launch.sh ./

RUN chmod +x ./launch.sh; # chown 2001 /usr/app

# No user defined. Set in manifest
# USER 2001

CMD ./launch.sh

