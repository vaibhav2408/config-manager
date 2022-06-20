#!/bin/bash -ex

# directory/directories where the auto-linting will be executed
SRC_DIRS=${1:-"adobe_config_mgmt_lib tests"}

echo "Running linting checks for source code in ${SRC_DIRS} with directory context $(pwd)"

for src_dir in ${SRC_DIRS}
do
    [ ! -d ./${src_dir} ] \
        && echo "Running lint check with incorrect directory context. Directory ${src_dir} not present" \
        && exit 1
done

#mypy \
#    --ignore-missing-imports \
#    adobe_config_mgmt_lib

black \
    --check \
    --diff \
    ${SRC_DIRS}

isort \
    --check-only \
    --profile black \
    ${SRC_DIRS}

# Use pyline to (only) generate a code similarity report to avoid large amounts
# of code duplication. (NOTE: only running on the adobe_config_mgmt_lib/ source code directory)
pylint \
    --disable=all \
    --enable=duplicate-code \
    --min-similarity-lines=20 \
    adobe_config_mgmt_lib

# Code complexity/quality checks
MIN_COMPLEXITY_GRADE="C"
complexity_check="radon cc --show-complexity --min=${MIN_COMPLEXITY_GRADE} adobe_config_mgmt_lib tests/unit_test"
complex_code="$(${complexity_check})"
if [[ ! -z "${complex_code}" ]]; then
    echo "Seeing overly complex code. Reach a minimum grade of ${MIN_COMPLEXITY_GRADE} for files below."
    echo "See https://radon.readthedocs.io/en/latest/intro.html for more info."
    exec ${complexity_check}
    exit 1
fi
