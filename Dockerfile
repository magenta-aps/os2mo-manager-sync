# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0

FROM python:3.11.2

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION="1.2.0" \
    POETRY_HOME=/opt/poetry \
    VIRTUAL_ENV="/venv"
ENV PATH="$VIRTUAL_ENV/bin:$POETRY_HOME/bin:$PATH"

# Install poetry in an isolated environment
RUN python -m venv $POETRY_HOME \
    && pip install --no-cache-dir poetry==${POETRY_VERSION}

# Install project in another isolated environment
WORKDIR /opt
RUN python -m venv $VIRTUAL_ENV
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --only=main

WORKDIR /opt/app
COPY sd_managerscript .
WORKDIR /opt/
CMD [ "uvicorn", "--factory", "app.main:create_app", "--host", "0.0.0.0" ]
