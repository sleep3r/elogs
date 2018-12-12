FROM ubuntu

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3.7 python3-pip python3-dev wget git vim curl npm libkrb5-dev

EXPOSE 80 8000 443 8085

COPY ./docker/pyodbc_mssql_driver.sh /srv/docker/
# installs ubuntu odbc drivers and pip django odbc packets
RUN /srv/docker/pyodbc_mssql_driver.sh

WORKDIR /srv

RUN pip3 install pipenv
COPY ./Pipfile.lock /srv
COPY ./Pipfile /srv
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1
RUN pipenv install --deploy --system --ignore-pipfile

COPY ./frontend /srv/frontend

WORKDIR /srv/frontend
RUN git clone https://github.com/creationix/nvm.git .nvm
WORKDIR ./.nvm
RUN git checkout v0.33.11
ENV NODE_OPTIONS --max_old_space_size=4096
RUN . ./nvm.sh \
  && nvm install 8.9.1 \
  && cd /srv/frontend \
  && npm --version \
  && npm install npm -g \ 
  && npm i \ 
  && npm run build

COPY . /srv
COPY ./docker/django/entrypoint /entrypoint
WORKDIR /srv

