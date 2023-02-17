#!/bin/zsh
#================================================================
# HEADER
#================================================================

export PROJECT=VANDAL
export ENV=Dev

export DB_HOST=http://localhost:4566
export DB_TABLE_LAYERS=${PROJECT}-${ENV}-ArtworkLayersTable
export DB_TABLE_MESSAGES=${PROJECT}-${ENV}-WebsocketMessagesTable
export DB_TABLE_USERS=${PROJECT}-${ENV}-UsersTable

export S3_HOST=http://localhost:4566
export S3_BUCKET_IMAGES=${PROJECT:l}-${ENV:l}-images-bucket # lowercase project and env

export USERPOOL_ID=us-east-1_LqZBLBRAs
export APP_CLIENT_ID=4c1tjq9el7roqs8r0gf0brlne9
# export APP_CLIENT_SECRET=157quigo4ns20j9kt02454efm6ob12tfun866du74pkagkkf7o8k

aws --endpoint-url=$S3_HOST s3 mb s3://$S3_BUCKET_IMAGES &&
aws --endpoint-url=$S3_HOST s3 sync ../_sample_data s3://$S3_BUCKET_IMAGES &&

uvicorn app.main:api --reload --host 127.0.0.1 --port 8080 --reload &&

curl -X POST -H "Content-Type: application/json" -d @../_sample_data/data.json http://localhost:8080/art/create
