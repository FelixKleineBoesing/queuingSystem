FROM python:3.7.0

RUN apt-get update && apt-get install dos2unix

ENV MLFLOW_HOME /opt/mlflow
ENV MLFLOW_VERSION 0.7.0
ENV SERVER_PORT 5001
ENV SERVER_HOST 0.0.0.0
ENV FILE_STORE ${MLFLOW_HOME}/fileStore
ENV ARTIFACT_STORE ${MLFLOW_HOME}/artifactStore

RUN pip install mlflow==${MLFLOW_VERSION} && \
    mkdir -p ${MLFLOW_HOME}/scripts && \
    mkdir -p ${FILE_STORE} && \
    mkdir -p ${ARTIFACT_STORE}

COPY ./misc/mlflow_run.sh ${MLFLOW_HOME}/scripts/run.sh
RUN chmod +x ${MLFLOW_HOME}/scripts/run.sh

RUN dos2unix ${MLFLOW_HOME}/scripts/run.sh

EXPOSE ${SERVER_PORT}/tcp

WORKDIR ${MLFLOW_HOME}

ENTRYPOINT ["./scripts/run.sh"]