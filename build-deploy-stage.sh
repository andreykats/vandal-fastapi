#!/bin/zsh
#================================================================
# HEADER
#================================================================

sam build --template template-stage.yaml && sam deploy --config-env staging