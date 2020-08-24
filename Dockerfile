FROM python:3.6-slim

ENV APP_DIR /usr/src/app
WORKDIR ${APP_DIR}

# Install gettext for python manage.py compilemessages
RUN apt-get update && apt-get install gettext -y

COPY ./requirements.txt ${APP_DIR}
RUN pip install --upgrade pip && pip install -r ./requirements.txt

COPY ./entrypoint.sh ${APP_DIR}
RUN chmod 0700 ./entrypoint.sh

COPY . ${APP_DIR}

# Compilesass and collect static inside building for faster container running
RUN python manage.py compilesass
RUN python manage.py collectstatic --noinput --clear

CMD ["sh", "entrypoint.sh"]
