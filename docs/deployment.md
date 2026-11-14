# Deployment Guide

## Local deployment

### Prerequisites

- Windows 11 with Docker Desktop and Docker Compose.
- Git.
- PowerShell.

### Start the stack

From the repository root:

```powershell
docker compose up -d --build
docker compose ps
```

The Compose stack contains PostgreSQL (`db`), Django/Gunicorn (`web`), and Nginx (`nginx`). Nginx publishes local port 80 and forwards traffic to the API service on port 8000.

### Verify the local service

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1/api/health/live/" -UseBasicParsing |
    Select-Object StatusCode, Content
```

Expected HTTP status: `200`.

### Stop the stack

```powershell
docker compose stop
```

Do not use `docker compose down -v` unless intentionally deleting the persistent database volume.

## Render deployment

The production service is configured in the Render dashboard and connected to the GitHub repository.

Production URL:

`https://pharmacy-management-platform.onrender.com`

The Render web service uses the Dockerfile and environment variables configured in the Render dashboard. The production database is a managed Render PostgreSQL service. Render terminates HTTPS; the local Nginx container is not required for the Render deployment.

### Production environment variables

Configure secrets in the Render dashboard, not in source control. Typical settings include:

- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=pharmacy-management-platform.onrender.com`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT=5432`

Use the actual values supplied by Render. Never place credentials in this document or commit them to Git.

### Verify production

- `https://pharmacy-management-platform.onrender.com/api/health/live/`
- `https://pharmacy-management-platform.onrender.com/api/health/ready/`

Expected status: HTTP `200`; readiness should report the database as connected.

## Deployment notes

- A push to the configured GitHub branch triggers the configured Render deployment.
- Review Render deploy logs after each deployment.
- Render free services and free database plans may have sleep/expiry limits; check the dashboard for current plan status.
