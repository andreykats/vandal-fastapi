# Vandal FastAPI Backend
Vandal Backend API Service

## Requirements
### Local
* pyenv
* Python 3.9.16
* Docker Desktop

### Remote
* AWS DynamoDB (PynamoDB)
* AWS S3
* AWS Lambda
* AWS CloudFormation (SAM CLI)
* AWS API Gateway


## Installation

### Install pyenv:

pyenv is a tool to manage multiple versions of Python. It is simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well.
* Mac:
```
brew update && brew install pyenv
```
* Linux:
```
curl https://pyenv.run | bash
```

### Install autoenv:
autoenv is a directory-based environment switcher for the shell. It's a tool that can be used to automatically `cd` into a directory and have it `source` a file, such as a `.env` file, to set environment variables.
```
curl -#fLo- 'https://raw.githubusercontent.com/hyperupcall/autoenv/master/scripts/install.sh' | sh
```

### Clone the repository:

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
pip freeze > requirements-dev.txt

pip freeze | xargs pip uninstall -y

sam build && sam local start-api

sam delete [stack-name]

sam build --template template-dev.yaml && sam local start-api -p 8080

sam build --template template-stage.yaml && sam deploy --template template-stage.yaml --config-env staging

sam deploy --template template-stage.yaml

sam deploy --config-env staging

sam deploy --template template-stage.yaml --config-env staging

sam build --template template-stage.yaml && sam deploy --config-env staging

```