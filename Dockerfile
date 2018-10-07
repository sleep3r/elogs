FROM ubuntu

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3.6 python3-pip python3-dev git vim nginx curl npm


RUN mkdir /srv/media /srv/static

EXPOSE 80 8000

VOLUME ["/srv/media/"]

COPY ./docker/pyodbc_mssql_driver.sh /srv/docker/
# installs ubuntu odbc drivers and pip django odbc packets
RUN /srv/docker/pyodbc_mssql_driver.sh

WORKDIR /srv

# COPY ./package.json /srv
# RUN npm i

RUN pip3 install pipenv
COPY ./Pipfile.lock /srv
COPY ./Pipfile /srv
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
RUN pipenv install --deploy --system --ignore-pipfile

COPY . /srv

# RUN ./node_modules/.bin/webpack
WORKDIR /srv/frontend
RUN git clone https://github.com/creationix/nvm.git .nvm
WORKDIR ./.nvm
RUN git checkout v0.33.11
RUN ls
ENV NODE_OPTIONS --max_old_space_size=4096
RUN . ./nvm.sh \
  && nvm install 8.9.1 \
  && cd /srv/frontend \
  && npm --version \
  && npm install npm -g \
  && npm i \
  && npm run build

ENV DJANGO_SETTINGS_MODULE config.settings.settings_aws
ENV DOCKER yes
ENV DEBUG False

