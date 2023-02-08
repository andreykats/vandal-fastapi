import uvicorn
from os import environ

# Set the environment variables for the local database
environ["DB_HOST"] = "http://localhost:8000"
environ["S3_IMAGE_BUCKET"] = "vandal-images-bucket-dev"
environ["S3_HOST"] = "http://localhost.localstack.cloud:4566"

if __name__ == "__main__":
    uvicorn.run("app.main:api", host="127.0.0.1", port=8080, reload=True)

# root_path="/stage"