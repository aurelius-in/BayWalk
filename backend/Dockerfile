FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install --no-cache-dir uv
COPY backend/requirements.in /app/backend/requirements.in
RUN uv pip install -r /app/backend/requirements.in --system && uv pip freeze > /app/backend/requirements.lock

COPY backend /app/backend
WORKDIR /app/backend

EXPOSE 8080
CMD ["gunicorn", "api.main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8080", "--threads", "4"]
