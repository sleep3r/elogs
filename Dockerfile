FROM ubuntu

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y python3-dev
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y nginx
RUN apt-get install -y curl
RUN apt-get install -y npm

RUN mkdir /srv/media /srv/static /srv/logs

EXPOSE 80

VOLUME ["/srv/media/", "/srv/logs/"]

COPY ./docker/pyodbc_mssql_driver.sh /srv/docker/
# installs ubuntu odbc drivers and pip django odbc packets
RUN /srv/docker/pyodbc_mssql_driver.sh

COPY ./requirements.txt /srv
RUN pip3 install -r /srv/requirements.txt

WORKDIR /srv

COPY ./package.json /srv
RUN npm i

COPY . /srv
RUN mkdir /srv/e-logs/logs
RUN mkdir /srv/e-logs/logs/main
RUN mkdir /srv/e-logs/logs/main_debug_calls
RUN mkdir /srv/e-logs/logs/main_debug_debug
RUN mkdir /srv/e-logs/logs/main_debug_error
RUN mkdir /srv/e-logs/logs/main_debug_info
RUN ./node_modules/.bin/webpack
ENV DJANGO_SETTINGS_MODULE config.settings.settings_singapore

ENTRYPOINT ["/srv/docker/entrypoint.sh"]
