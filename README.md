# Vandal {working title} Backend
Python API Service

## Requirements

* pyenv
* Python 3.9
* FastAPI
* Docker Desktop
* AWS DynamoDB (PynamoDB)
* AWS S3
* AWS Lambda
* AWS CloudFormation (SAM CLI)
* AWS API Gateway


## Installation

```
git clone git@github.com:andreykats/vandal-fastapi.git
```

### Set Python version:
In the project directory, run:

```
pyenv install 3.9.16 && pyenv local 3.9.16
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
pip install -r requirements-dev.txt
```

### Start database container:
In the project directory, run:

```
docker-compose up -d
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
python app/run.py
```

## Admin
```
pip freeze > requirements.txt

pip freeze | xargs pip uninstall -y

sam build && sam local start-api

sam delete [stack-name]


```