
$ErrorActionPreference = "Stop"

$projectRoot = Split-Path $PSScriptRoot -Parent
$backupDir = Join-Path $projectRoot "backups"

New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$fileName = "pharmacy_backup_$timestamp.dump"
$containerPath = "/tmp/$fileName"
$backupPath = Join-Path $backupDir $fileName

Write-Host "Starting PostgreSQL backup..."

docker compose exec -T db sh -c "pg_dump -U `"`$POSTGRES_USER`" -d `"`$POSTGRES_DB`" -Fc -f $containerPath"

if ($LASTEXITCODE -ne 0) {
    throw "Database backup failed."
}

docker compose cp "db:$containerPath" $backupPath

if ($LASTEXITCODE -ne 0) {
    throw "Backup copy failed."
}

docker compose exec -T db rm -f $containerPath

if ($LASTEXITCODE -ne 0) {
    Write-Warning "Temporary backup cleanup failed."
}

Write-Host ""
Write-Host "Backup completed successfully!" -ForegroundColor Green
Write-Host "Location: $backupPath"
Write-Host "Size: $((Get-Item $backupPath).Length) bytes"
