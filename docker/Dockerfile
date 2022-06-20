# first stage
FROM python:3.8 AS builder
# Install dependencies
RUN apt-get update

RUN pip install poetry

ENV APP_ROOT_DIR=/opt/adobe


ENV POETRY_VERSION=1.0.9
# direct poetry to install at this location
ENV POETRY_HOME="/opt/poetry"
# no interaction during poetry installs
ENV POETRY_NO_INTERACTION=1
# python deps root
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PIP_VENV_VERSION=20.1.1
ENV PATH="${POETRY_HOME}/bin:${APP_ROOT_DIR}/.venv/bin:${PATH}"


RUN mkdir -p $APP_ROOT_DIR
WORKDIR $APP_ROOT_DIR


COPY ./pyproject.toml ./pyproject.toml
COPY ./scripts ./scripts

RUN poetry install --no-dev

# Copy the application source files only after installing the dependencies is
#  important to save image build time when only source code files are changed.
COPY ./adobe_config_mgmt_lib ./adobe_config_mgmt_lib

ENV PYTHONPATH=$PYTHONPATH:/${APP_ROOT_DIR}/adobe_config_mgmt_lib

EXPOSE 5000
CMD ["poetry", "run"]
