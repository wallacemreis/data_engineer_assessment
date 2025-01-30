FROM python:3.11-slim

RUN pip install duckdb

WORKDIR /app
COPY import_postgres_to_duckdb.py .

CMD ["python", "import_postgres_to_duckdb.py"]