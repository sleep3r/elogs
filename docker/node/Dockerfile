FROM ubuntu
RUN ls
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y wget git vim curl npm

EXPOSE 80 8000 443 8085 8003

RUN git clone https://tlenbit:cd37654c9db8b59940b94c4caf9dd64922f8e099@github.com/Resolim/e-logs-constructor.git /e-logs-constructor
WORKDIR /e-logs-constructor
RUN git checkout develop

COPY ./docker/node/entrypoint  /entrypoint

RUN git clone https://github.com/creationix/nvm.git .nvm
WORKDIR ./.nvm
RUN git checkout v0.33.11
ENV NODE_OPTIONS --max_old_space_size=4096
RUN . ./nvm.sh \
  && nvm install 8.9.1 \
  && npm --version \
  && npm install npm -g \ 
  && cd /e-logs-constructor/frontend \
  && npm install http-server \
  && npm i \
  && npm run build \
  && cd /e-logs-constructor/backend \
  && npm i

