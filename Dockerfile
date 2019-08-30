FROM python:3.7-alpine

ENV FLASK_APP flasky.py
ENV FLASK_CONFIG docker

RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky

COPY Pipfile-docker Pipfile
RUN python3.7 -m pip install pipenv --user
ENV PATH "/home/flasky/.local/bin:${PATH}"
RUN pipenv --python 3.7
RUN pipenv update

COPY app app
COPY migrations migrations
COPY flasky.py config.py boot.sh ./

USER root
RUN chmod +x boot.sh

USER flasky

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

