# Vandal {working title} Backend
Python API Service

## Requirements

Python 3.10

https://www.python.org/downloads/

Docker Desktop

https://www.docker.com/products/docker-desktop

DynamoDB-Local

https://hub.docker.com/r/amazon/dynamodb-local



## Installation

```
git clone git@github.com:andreykats/vandal-fastapi.git
```

### Initialize virtual environment:
In the project directory, run:

```
python -m venv .venv
```

### Activate virtual environment:
In the project directory, run:

```
source .venv/bin/activate
```

### Install dependencies:

In the project directory, run:

```
pip install -r requirements.txt
```

## Running

### Activate virtual environment if deactivated:
In the project directory, run:

```
source .venv/bin/activate
```


### Start on localhost:
In the project directory, run:
```
python run.py
```

## Admin
Update requirements file when installing new packages:
```
pip3 freeze > requirements.txt
```