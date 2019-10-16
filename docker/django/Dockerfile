FROM python:3.7

ENV NODE_OPTIONS --max_old_space_size=4096
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y npm && \
    pip3 install --upgrade pip pipenv && \
    npm install npm@latest -g

WORKDIR /srv
COPY ./Pipfile.lock ./Pipfile /srv/
RUN pipenv install --deploy --system --ignore-pipfile

WORKDIR /srv/frontend
COPY ./frontend /srv/frontend
RUN npm i && npm run build

COPY . /srv
COPY ./docker/django/entrypoint /entrypoint
COPY ./docker/django/apply_migrations.sh /apply_migrations.sh
WORKDIR /srv

EXPOSE 80 8000 443 8085
ENTRYPOINT ["/entrypoint"]
