# Small, official Python base image
FROM python:3.12-slim

# Don't write .pyc files; show logs immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install dependencies first so Docker can cache this layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Run as a non-root user (a basic security practice interviewers ask about)
RUN useradd --create-home appuser
USER appuser

EXPOSE 8080

# Docker checks the /health endpoint every 30 seconds
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# gunicorn is a production web server; 2 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
