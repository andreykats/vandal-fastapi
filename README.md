# Vandal {working title} Backend
Python API Service

## Requirements

Python 3.11

https://www.python.org/downloads/

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

Usage: 
`uvicorn project_dir.project_file.fastapi_instance --reload`

```
uvicorn app.main:api --reload --host 0.0.0.0 --port 8000
```

## Admin
Update requirements file when installing new packages:
```
pip3 freeze > requirements.txt
```