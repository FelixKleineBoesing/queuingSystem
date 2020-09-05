FROM python:3.7
ENV PYTHONPATH=/
ENV PYTHONUNBUFFERED=1

# copy installation loop and convert to unix
RUN apt-get update && apt-get install -y dos2unix
COPY ./loop_installation.sh /tmp/loop_installation.sh
RUN dos2unix /tmp/loop_installation.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*

COPY ./src/api/requirements.txt /src/api/requirements.txt
COPY ./src/misc/requirements.txt /src/misc/requirements.txt
COPY ./src/controller/requirements.txt /src/controller/requirements.txt
COPY ./src/data_access/requirements.txt /src/data_access/requirements.txt
COPY ./src/modelling/requirements.txt /src/modelling/requirements.txt
COPY ./src/tasks/requirements.txt /src/tasks/requirements.txt

RUN bash /tmp/loop_installation.sh

COPY ./src/__init__.py /src/__init__.py
COPY ./src/data_access /src/data_access
COPY ./src/api /src/api
COPY ./src/misc /src/misc
COPY ./src/modelling /src/modelling
COPY ./src/controller /src/controller
COPY ./src/tasks /src/tasks

