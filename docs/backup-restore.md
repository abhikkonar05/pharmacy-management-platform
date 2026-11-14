# Backup and Restore

## Purpose

The project includes PowerShell scripts for creating a PostgreSQL backup and restoring a backup into a target database. Backups are stored under the local `backups/` directory and are excluded from Git.

## Create a backup

From the project root in PowerShell:

```powershell
.\scripts\backup.ps1
```

The script creates a timestamped PostgreSQL custom-format dump in `backups/`.

## Validate a backup archive

Use the actual dump filename produced by the backup script:

```powershell
docker compose exec -T db pg_restore -l /path/to/backup.dump
```

If the script copies the archive into the database container under `/tmp`, use that container path instead.

## Restore test

The restore procedure was tested against a separate test database named `pharmacy_restore_test`; the live/local application database was not used as the restore target during that test.

Run the repository's restore script with its documented parameters:

```powershell
Get-Content .\scripts\restore.ps1
```

Then run it using the parameters defined in that script. Do not guess parameter names.

## Safety notes

- Never run `docker compose down -v` as a routine troubleshooting step; it removes the named database volume.
- Do not commit `.env`, database passwords, API tokens, or `.dump` files.
- Before restoring to a production database, take a fresh backup and verify the target database name.
- Keep backup files in a protected location and periodically test restoration.

## Evidence

The project owner tested creation of a custom-format dump, inspected the archive with `pg_restore -l`, and restored it into a separate test database. Record the exact backup filename and test date in the final submission evidence.
