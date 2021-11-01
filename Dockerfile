FROM node:16

RUN apt update -y \
  && apt install -y python3 python3-pip

WORKDIR /usr/src/app

RUN mkdir web

COPY requirements.txt .

COPY web/package.json web/.

RUN pip3 install -r requirements.txt \
  && npm install --prefix ./web

ENV PATH /usr/src/app/web/node_modules/.bin:$PATH

COPY . .

#CMD python3 build.py