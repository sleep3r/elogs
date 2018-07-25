FROM ubuntu

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y python3-dev
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y nginx
RUN apt-get install -y curl

RUN mkdir /srv/media /srv/static /srv/logs

VOLUME ["/srv/media/", "/srv/logs/"]

COPY ./docker/pyodbc_mssql_driver.sh /srv/docker/
COPY ./requirements.txt /srv

# installs ubuntu odbc drivers and pip django odbc packets
RUN /srv/docker/pyodbc_mssql_driver.sh

RUN pip3 install -r /srv/requirements.txt

EXPOSE 80

WORKDIR /srv

COPY . /srv

ENTRYPOINT ["/srv/docker/entrypoint.sh"]
