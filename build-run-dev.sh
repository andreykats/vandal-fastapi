#!/bin/zsh
#================================================================
# HEADER
#================================================================

sam build --template template-dev.yaml && sam local start-api --port 8080 --warm-containers EAGER