# Rollback and Recovery

## Purpose

This runbook describes a cautious rollback approach for the deployed Pharmacy Management Platform.

## Application rollback

1. Identify the last known-good commit in GitHub.
2. In the Render dashboard, open the web service's Events/Deploys history.
3. If a previous successful deploy is available, use Render's rollback/redeploy option for that deploy.
4. Wait for deployment to finish.
5. Verify:
   - `/api/health/live/`
   - `/api/health/ready/`
   - One authenticated read-only API endpoint.
6. Review Render logs for startup errors.

If the platform does not offer a direct rollback for the selected deploy, revert the problematic commit in Git and push the revert. Confirm the CI workflow passes before relying on the new deployment.

## Database recovery

Application rollback does not automatically reverse database schema or data changes. Before a production database restore:

1. Take a fresh backup of the current database.
2. Confirm the backup archive is readable.
3. Confirm the exact target database.
4. Restore only with an approved maintenance plan because restoring can overwrite current data.
5. Recheck readiness and key API endpoints.

## Local container recovery

```powershell
docker compose restart web
docker compose ps
```

Then verify:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1/api/health/live/" -UseBasicParsing
```

The application restart recovery test was observed to return HTTP 200.

## Safety

- Never delete the persistent Docker volume as a first-line recovery action.
- Keep database restore separate from application rollback.
- Record the failed deployment, selected recovery point, actions, and verification results.
