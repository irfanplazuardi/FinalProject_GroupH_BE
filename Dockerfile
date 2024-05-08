# Gunakan gambar Python resmi
FROM python:3.12-slim

# Set variabel lingkungan untuk Poetry dan versi yang diinginkan
ENV POETRY_VERSION=1.8
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Atur variabel lingkungan yang diperlukan untuk aplikasi
ENV DATABASE_USERNAME=root
ENV DATABASE_PASSWORD=QiQGMDlvPYvHUmXBjFtiLYSIRNXXhcRl
ENV DATABASE_URL=monorail.proxy.rlwy.net:34808
ENV DATABASE_NAME=quality_education
ENV SECRET_KEY=MYSECRETKEY

# Instal Poetry
RUN python3 -m venv $POETRY_VENV && \
    $POETRY_VENV/bin/pip install --upgrade pip setuptools && \
    $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Tambahkan Poetry ke PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Set direktori kerja
WORKDIR /app

# Salin file yang diperlukan ke dalam gambar
COPY poetry.lock pyproject.toml /app/

# Instal dependencies
RUN poetry install --no-root

# Salin seluruh kode aplikasi ke direktori kerja
COPY . /app

# Tentukan port yang akan dibuka
EXPOSE 8080

# Gunakan CMD untuk menjalankan aplikasi
CMD ["/bin/bash", "docker-entrypoint.sh"]
