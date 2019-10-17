FROM nikolaik/python-nodejs:python3.8-nodejs12

ENV NODE_OPTIONS --max_old_space_size=4096
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1

#RUN curl -sL https://deb.nodesource.com/setup_12.x  | bash -
RUN apt-get update && apt-get -y upgrade && \
    npm install -g npm@latest && npm upgrade -g && \
    npm install -g @vue/cli && \
    pip3 install --upgrade pip pipenv

COPY ./Pipfile.lock ./Pipfile /srv/
COPY ./frontend/package.json ./frontend/package-lock.json /srv/frontend/
RUN cd /srv/frontend/ && npm ci && \
    cd /srv/ && pipenv install --deploy --system --skip-lock

#--ignore-pipfile

WORKDIR /srv/frontend
COPY ./frontend /srv/frontend
RUN npm run build

COPY . /srv
WORKDIR /srv
RUN chmod 777 /srv/docker/django/entrypoint /srv/docker/django/apply_migrations.sh && \
    cp /srv/docker/django/entrypoint /srv/docker/django/apply_migrations.sh / && \
    python3 manage.py collectstatic --noinput && \
    mkdir -p /srv/frontend/dist/static && \
    cp -r /srv/staticfiles/* /srv/frontend/dist/static/

EXPOSE 80 8000 443 8085
ENTRYPOINT ["/entrypoint"]
