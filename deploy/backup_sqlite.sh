#!/bin/sh
# Backup diario do SQLite do RadarPromo. Rodar via cron no host (nao dentro
# do container), ex.: 0 3 * * * /opt/radarpromo/deploy/backup_sqlite.sh
set -eu

PROJETO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DB_PATH="$PROJETO_DIR/data/radarpromo.db"
BACKUP_DIR="$PROJETO_DIR/backups"
DATA="$(date +%F)"

mkdir -p "$BACKUP_DIR"
sqlite3 "$DB_PATH" ".backup '$BACKUP_DIR/radarpromo-$DATA.db'"

# Mantem so os ultimos 14 backups.
find "$BACKUP_DIR" -name 'radarpromo-*.db' -mtime +14 -delete
