#!/bin/zsh
#================================================================
# HEADER
#================================================================

export VANDAL_ENV=dev

# export DB_HOST=http://localhost:8000
export DB_HOST=http://localhost:4566
export DB_TABLE_LAYERS=vandal-table-layers-dev
export DB_TABLE_MESSAGES=vandal-table-messages-dev

export S3_HOST=http://localhost:4566
export S3_BUCKET_IMAGES=vandal-bucket-images-dev

aws --endpoint-url=$S3_HOST s3 mb s3://$S3_BUCKET_IMAGES &&
aws --endpoint-url=$S3_HOST s3 sync images s3://$S3_BUCKET_IMAGES &&

uvicorn app.src.main:api --reload --host 127.0.0.1 --port 8080 --reload &&

curl -X POST -H "Content-Type: application/json" -d @./sample_data.json http://localhost:8080/art/create
