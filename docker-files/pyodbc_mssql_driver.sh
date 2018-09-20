#!/bin/bash

# "Microsoft ODBC Driver 17 for SQL Server" installation instructions for ubuntu 18.04 (!!!) 
# from official microsoft website
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
yes | ACCEPT_EULA=Y apt-get install msodbcsql17
# optional: for bcp and sqlcmd
yes | ACCEPT_EULA=Y apt-get install mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
yes | apt-get install unixodbc-dev

pip3 install django-pyodbc-azure
