#!/bin/bash -ex

#
# Start the adobe_config_mgmt_lib locally for development. Run a celery worker & celery beat in the background.
#

PORT=${1:-5000}


export PYTHONPATH=$PYTHONPATH:$(pwd)/adobe_config_mgmt_lib

# Activate the python venv.
source "$(poetry env info --path)/bin/activate"



uvicorn \
    --reload \
    --host 0.0.0.0 \
    --port ${PORT} \
    --log-level debug \
    --use-colors \
    main:app
