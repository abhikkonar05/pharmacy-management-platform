# Pharmacy Management Platform

## Project Overview

A Pharmacy Inventory Management API developed as an internship project for Algions AI Labs.

The application manages medicines, batches, stock movements and inventory reports.

## Technology Stack

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL 16
- Docker and Docker Compose
- Nginx
- Gunicorn
- GitHub Actions
- Render

## Main Features

- Medicine management
- Batch-level inventory management
- Purchase, sale, return and adjustment records
- Expiry date validation
- Prevention of negative stock
- Prevention of concurrent overselling
- Stock movement audit history
- Inventory reports
- Token-based authentication
- Health and readiness endpoints

## Local Setup

1. Clone the repository:

   `git clone https://github.com/abhikkonar05/pharmacy-management-platform.git`

2. Open the project directory:

   `cd pharmacy-management-platform`

3. Configure the required database environment variables in `.env`.

4. Start the application:

   `docker compose up -d --build`

5. Check running containers:

   `docker compose ps`

## Application URLs

| Service | URL |
|---|---|
| Homepage | http://localhost/ |
| Admin | http://localhost/admin/ |
| Health | http://localhost/api/health/ |
| Liveness | http://localhost/api/health/live/ |
| Readiness | http://localhost/api/health/ready/ |
| Medicines | http://localhost/api/medicines/ |
| Batches | http://localhost/api/batches/ |
| Stock Movements | http://localhost/api/stock-movements/ |
| Reports | http://localhost/api/reports/ |
| Token Authentication | http://localhost/api/auth/token/ |

Protected API endpoints require token authentication.

## Nginx Reverse Proxy

Nginx listens on port 80 and forwards requests to the Django Gunicorn service through the internal Docker network.

Configuration file: `nginx/default.conf`

## Database Backup and Restore

PowerShell scripts:

- `scripts/backup.ps1`
- `scripts/restore.ps1`

The project includes backup and restore procedures for PostgreSQL.

## CI/CD

GitHub Actions workflow:

`.github/workflows/ci-cd.yml`

The workflow performs lint checks, Django checks, migration checks, automated tests and Docker image builds.

## Deployment

The application is deployed on Render.

Live URL: https://pharmacy-management-platform.onrender.com

## Security

- Environment-based configuration
- Token-based API authentication
- Secrets excluded from Git
- Non-root Docker application user
- Persistent PostgreSQL storage

## Project Purpose

This project demonstrates pharmacy inventory management, API development, containerization, CI/CD and deployment practices.
