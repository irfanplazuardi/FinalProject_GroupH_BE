FROM python:latest as python-base

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.8
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Create stage for Poetry installation
FROM python-base as poetry-base

# Install necessary tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Create a new stage from the base python image
FROM python-base as example-app

# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

# Copy Dependencies
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR
# Copy Application
COPY . /app

RUN poetry install


EXPOSE 5000

# Run Application

CMD ["poetry", "run", "flask", "run"]