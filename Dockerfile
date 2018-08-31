FROM ubuntu

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3.6 python3-pip python3-dev git vim nginx curl npm


RUN mkdir /srv/media /srv/static

EXPOSE 80

VOLUME ["/srv/media/"]

COPY ./docker/pyodbc_mssql_driver.sh /srv/docker/
# installs ubuntu odbc drivers and pip django odbc packets
RUN /srv/docker/pyodbc_mssql_driver.sh

WORKDIR /srv

COPY ./package.json /srv
RUN npm i

RUN pip3 install pipenv
COPY ./Pipfile.lock /srv
COPY ./Pipfile /srv
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
RUN pipenv install --deploy --system --ignore-pipfile

COPY . /srv

RUN ./node_modules/.bin/webpack

ENTRYPOINT ["/srv/docker/entrypoint.sh"]
