import uvicorn
from os import environ

# Set the environment variables for the local database
environ["DB_HOST"] = "http://localhost:8000"

if __name__ == "__main__":
    uvicorn.run("src.main:api", host="127.0.0.1", port=8080, reload=True)

# root_path="/stage"