FROM python:3.12-slim as python-base

ENV POETRY_VERSION=1.8
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

ENV DATABASE_USERNAME=root
ENV DATABASE_PASSWORD=QiQGMDlvPYvHUmXBjFtiLYSIRNXXhcRl
ENV DATABASE_URL=monorail.proxy.rlwy.net:34808
ENV DATABASE_NAME=quality_education
ENV SECRET_KEY=MYSECRETKEY

# Create stage for Poetry installation
FROM python-base as poetry-base

# Retry logic for installing Poetry
RUN set -e && \
    for i in 1 2 3; do \
        python3 -m venv $POETRY_VENV && \
        $POETRY_VENV/bin/pip install -U pip setuptools && \
        $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION} && break || sleep 5; \
    done

# Create a new stage from the base python image
FROM python-base as example-app

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

EXPOSE 8080

COPY . /app

WORKDIR /app

# Copy Dependencies
COPY poetry.lock pyproject.toml ./

# [OPTIONAL] Validate the project is properly configured

# Install Dependencies
RUN poetry install --no-root

# Copy Application
# Run Application
CMD ["/bin/bash", "docker-entrypoint.sh"]
