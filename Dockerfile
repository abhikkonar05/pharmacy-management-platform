
# Python base image
FROM python:3.12-slim

# Python environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy Django backend
COPY backend/ .

# Create non-root application user
RUN groupadd --system app \
    && useradd --system --gid app --create-home app \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R app:app /app

# Run as non-root user
USER app

# Application port
EXPOSE 8000

# Start Django using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "config.wsgi:application"]
