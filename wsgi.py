#!/user/bin/env python
import os
import click
from pathlib import Path
from dotenv import load_dotenv
from app import create_app, db, models
from backup import restore_from_backup, BACKUP_FILENAME_POSTFIX

INIT_DB_CMD = (
    "poetry run flask db init",
    "poetry run flask db migrate",
    "poetry run flask db upgrade"
)

BACKUP_DIR = os.environ.get("BACKUP_DIR")

load_dotenv()

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, models=models)


@app.cli.command()
def restore_db_from_backup(backup_number=1):

    try:
        backup_number = int(backup_number)
    except ValueError:
        return

    all_backups = [f for f in os.listdir(BACKUP_DIR) if (Path(BACKUP_DIR) / f).is_file()]
    all_timestamps = []

    for backup in all_backups:
        backup_timestamp = backup.split(BACKUP_FILENAME_POSTFIX)[0]
        try:
            backup_timestamp = float(backup_timestamp)
            all_timestamps.append(backup_timestamp)
        except ValueError:
            continue

    all_timestamps.sort()
    restore_from_backup(all_timestamps[backup_number - 1])


@app.cli.command()
def create_db():
    """Create the configured database."""
    for cmd in INIT_DB_CMD:
        os.system(cmd)


@app.cli.command()
@click.confirmation_option(prompt="Drop all database tables?")
def drop_db():
    """Drop the current database."""
    db.drop_all()


if __name__ == "__main__":
    app.run()
