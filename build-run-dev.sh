#!/bin/zsh
#================================================================
# HEADER
#================================================================

sam build --template template-dev.yaml && sam local start-api -p 8080