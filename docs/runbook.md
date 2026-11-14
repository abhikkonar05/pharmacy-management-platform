# Operations Runbook

## Service overview

| Component | Local service/container | Purpose |
|---|---|---|
| Django + Gunicorn | `web` / `pharmacy-api` | REST API |
| PostgreSQL | `db` / `pharmacy-db` | Persistent database |
| Nginx | `nginx` / `pharmacy-nginx` | Local reverse proxy |

## Start and inspect

```powershell
docker compose up -d
docker compose ps
```

## Check application health

Local:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1/api/health/live/" -UseBasicParsing
Invoke-WebRequest -Uri "http://127.0.0.1/api/health/ready/" -UseBasicParsing
```

Production:

- `https://pharmacy-management-platform.onrender.com/api/health/live/`
- `https://pharmacy-management-platform.onrender.com/api/health/ready/`

## View logs

```powershell
docker compose logs --tail 100 web
docker compose logs --tail 100 db
docker compose logs --tail 100 nginx
```

## Restart the API

```powershell
docker compose restart web
```

After restart, check the live endpoint again.

## Common troubleshooting

### API is unavailable

1. Run `docker compose ps`.
2. Inspect `docker compose logs --tail 100 web`.
3. Confirm the database container is healthy.
4. Check Nginx logs if the API container is running but the public local URL fails.

### Database connection issue

1. Check `docker compose ps`.
2. Inspect database logs.
3. Confirm environment variable names are set in the local `.env` file.
4. Never paste passwords into tickets, chat, or logs.

### Authentication returns 401

- Obtain a fresh token from `POST /api/auth/token/`.
- Send `Authorization: Token <token>` for protected endpoints.
- Do not share the token.

### API returns 500

- Inspect application logs.
- Check Render deploy logs for production issues.
- Do not expose secrets or full database connection strings when sharing logs.

## Security and operational hygiene

- Keep secrets in environment variables or the hosting provider's secret settings.
- Keep `.env`, backups, and database dumps out of Git.
- Review Trivy findings and update affected base-image/system packages and Python build tools through a tested change.
- Do not claim a clean security scan while known findings remain.
- Keep a verified backup before risky database operations.
