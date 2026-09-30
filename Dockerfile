FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    freetds-dev \
    freetds-bin \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ ./src/

ENV PYTHONPATH=/app/src
ENV FLASK_ENV=production
ENV PORT=9999

EXPOSE 9999

CMD ["python", "src/app.py"]
