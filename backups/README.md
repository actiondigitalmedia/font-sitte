# Backups

Dated snapshots of `free-font-site/` + `memory-bank/`.

## Create a new backup
```bash
python3 scripts/backup_project.py
```

## Latest snapshot
See `LATEST.txt` for the most recent backup folder name.

## Restore
Copy contents from a snapshot folder back to repo root:
```bash
cp -a backups/font-sitte_YYYY-MM-DD_HHMMSS/free-font-site/ ./
cp -a backups/font-sitte_YYYY-MM-DD_HHMMSS/memory-bank/ ./
```

Each snapshot includes a `manifest.json` with metadata.
