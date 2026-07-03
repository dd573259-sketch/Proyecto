FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    pkg-config \
    default-libmysqlclient-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

    
COPY Proyecto_GP4/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8000


CMD python Proyecto_GP4/manage.py migrate --noinput && \
    python Proyecto_GP4/manage.py createsuperuser --noinput || true && \
    python Proyecto_GP4/manage.py runserver 0.0.0.0:${PORT:-8000}