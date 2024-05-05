FROM python:3.12

RUN mkdir /openid

COPY . /openid

WORKDIR /openid

RUN pip install pyjwt[crypto]

ENTRYPOINT python -u /openid/server.py