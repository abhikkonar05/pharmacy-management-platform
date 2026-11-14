
param(
    [Parameter(Mandatory = $true)]
    [string]$BackupFile,

    [string]$TargetDatabase = "pharmacy_restore_test"
)

$ErrorActionPreference = "Stop"

if ($TargetDatabase -notmatch '^[a-zA-Z][a-zA-Z0-9_]*$') {
    throw "Invalid database name."
}

if ($TargetDatabase -eq "pharmacy_db") {
    throw "Cannot restore directly into the production database."
}

if (-not (Test-Path $BackupFile)) {
    throw "Backup file not found."
}

$BackupFile = (Resolve-Path $BackupFile).Path

Write-Host "Starting restore..."

docker compose cp $BackupFile db:/tmp/restore_test.dump

if ($LASTEXITCODE -ne 0) {
    throw "Backup copy failed."
}

docker compose exec -T db sh -c 'createdb -U "$POSTGRES_USER" "$1"' sh $TargetDatabase

if ($LASTEXITCODE -ne 0) {
    throw "Could not create target database. Does it already exist?"
}

docker compose exec -T db sh -c 'pg_restore -U "$POSTGRES_USER" -d "$1" --no-owner --no-privileges /tmp/restore_test.dump' sh $TargetDatabase

if ($LASTEXITCODE -ne 0) {
    throw "Restore failed."
}

docker compose exec -T db rm -f /tmp/restore_test.dump

Write-Host ""
Write-Host "Restore completed successfully!" -ForegroundColor Green
Write-Host "Database: $TargetDatabase"
