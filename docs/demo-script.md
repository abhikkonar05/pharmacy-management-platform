# 3–5 Minute Project Demo Script

## 1. Introduction (20–30 seconds)

"This is a Pharmacy Management Platform API built with Django REST Framework and PostgreSQL. It manages medicines, batches, stock movements, and reports. The project is containerized with Docker Compose, uses Nginx locally, and is deployed on Render."

## 2. Show the deployed service (30 seconds)

Open:

- `https://pharmacy-management-platform.onrender.com/`
- `https://pharmacy-management-platform.onrender.com/api/health/live/`
- `https://pharmacy-management-platform.onrender.com/api/health/ready/`

Explain that the live endpoint checks whether the application process is running and the ready endpoint also checks database connectivity.

## 3. Show API endpoints (60–90 seconds)

In Postman, show successful authenticated requests:

- `POST /api/auth/token/`
- `GET /api/medicines/`
- `GET /api/batches/`
- `GET /api/stock-movements/`
- `GET /api/reports/`

Show the health endpoints without authentication.

Do not display or share the token in the recording.

## 4. Explain stock safety (45–60 seconds)

Explain that stock purchases, sales, returns, and adjustments are represented by stock movement records. The service validates quantities, rejects expired-batch sales and insufficient stock, and uses a database transaction with row-level locking.

If a safe demo dataset is already present, show a rejected sale and confirm the quantity did not change. Do not create destructive test data in production.

## 5. DevOps evidence (45–60 seconds)

Show:

- Docker Compose services running locally.
- GitHub Actions latest successful workflow.
- Render deployment and HTTPS.
- Backup archive and restore-test evidence.
- Trivy scan output, noting that vulnerabilities were reported and remain unresolved unless subsequently remediated.

## 6. Closing (10 seconds)

"The project demonstrates API development, containerization, CI checks, cloud deployment, health monitoring, and database backup/restore."

## Presenter reminders

- Use a test account and synthetic data.
- Hide passwords, tokens, `.env` values, and database connection strings.
- Do not claim the Trivy scan is clean; report the findings accurately.
