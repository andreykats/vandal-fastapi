#!/bin/zsh
#================================================================
# HEADER
#================================================================

# sam build && sam deploy  --config-env production

sam build --use-container --container-env-var-file env.json && sam deploy --config-env production --container-env-var-file env.json