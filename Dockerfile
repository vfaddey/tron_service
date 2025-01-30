FROM python:3.10.4-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"]