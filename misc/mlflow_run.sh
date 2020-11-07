#!/bin/sh

mlflow server \
    --backend-store-uri postgresql://$POSTGRES_USER:$POSTGRES_PASSWPORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB \
    --default-artifact-root $ARTIFACT_STORE \
    --host $SERVER_HOST \
    --port $SERVER_PORT