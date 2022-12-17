# Vandal {working title} Backend
Python API Service

## Installation

```
git clone git@github.com:andreykats/vandal-fastapi.git
```

Activate virtual environment:

```
source .venv/bin/activate
```

Install dependencies:

```
pip3 install -r requirements.txt
```

## Running
Running in development on localhost:
usage: uvicorn project_dir.project_file.fastapi_instance --reload

```
uvicorn app.main:api --reload
```

## Troubleshooting
Update requirements file when insalling new packages:
```
pip3 freeze > requirements.txt
```