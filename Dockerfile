# Python 3.10 official image
FROM python:3.10-alpine3.16

ENV APP_PATH=/app
ENV MIGRATION_PATH=$APP_PATH/migrations
ENV APP_SRC_PATH=$APP_PATH/src
ENV VIRTUAL_ENV=$APP_PATH/venv

# Update and upgrade container before anything else
RUN apk update && apk upgrade

# Add a bunch of dependencies needed to run correctly bcrypct and uwsgi
RUN apk add --no-cache linux-headers g++ postgresql-dev gcc build-base linux-headers ca-certificates python3-dev libffi-dev libressl-dev libxslt-dev

# Update pip to avoid annoying message
RUN pip install --upgrade pip

# Add dependency to run correctly psycopg2
RUN pip wheel --wheel-dir=/root/wheels psycopg2

# Add dependency to run correctly bcrypt
RUN pip wheel --wheel-dir=/root/wheels cryptography

# Create directory src, and copy our folder /src to inside of the container
RUN mkdir -p $APP_PATH
RUN mkdir -p $MIGRATION_PATH
RUN mkdir -p $APP_SRC_PATH

# Create a virtual python env for the src and set it as default in the global path
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY /src $APP_SRC_PATH
COPY /migrations $MIGRATION_PATH
COPY /main.py $APP_PATH

# Install all libraries
RUN pip install --no-cache-dir -r $APP_SRC_PATH/requirements.txt

WORKDIR $APP_PATH

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["flask", "run"]
