FROM ubuntu

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3.6 python3-pip python3-dev wget git vim curl npm libkrb5-dev

# Install caddy
RUN wget https://github.com/mholt/caddy/releases/download/v0.11.0/caddy_v0.11.0_linux_amd64.tar.gz
RUN tar -xzf caddy*.tar.gz caddy
RUN mv ./caddy /usr/local/bin

EXPOSE 80 8000 443 8085

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
# RUN pipenv lock
RUN pipenv install --deploy --system --ignore-pipfile

COPY ./frontend /srv/frontend

RUN pwd
RUN git clone https://tlenbit:cd37654c9db8b59940b94c4caf9dd64922f8e099@github.com/Resolim/e-logs-constructor.git /srv/e-logs-constructor
WORKDIR /srv/e-logs-constructor
RUN git checkout develop
# COPY ./e-logs-constructor /srv/e-logs-constructor

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
  && npm run build \
  && cd /srv/e-logs-constructor/frontend \
  && npm i \
  && npm run build \
  && cd /srv/e-logs-constructor/backend \
  && npm i

COPY . /srv
WORKDIR /srv

ENV DJANGO_SETTINGS_MODULE config.settings.settings_aws
ENV DOCKER yes
ENV DEBUG False

