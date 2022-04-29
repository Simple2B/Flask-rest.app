import os
import time
from pathlib import Path
from celery import Celery
from dotenv import load_dotenv
from backup import make_backup, BACKUP_FILENAME_POSTFIX


BACKUP_MAX_COUNT = 10
BACKUP_PERIOD = 60 * 60 * 24
BACKUP_DIR = os.environ.get("BACKUP_DIR")

load_dotenv()

REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_ADDR = os.environ.get("REDIS_ADDR", f"localhost:{REDIS_PORT}")
BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_ADDR}"

app = Celery('tasks', broker=BROKER_URL)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(BACKUP_PERIOD, do_backup.s())


@app.task
def do_backup():
    all_backups = [f for f in os.listdir(BACKUP_DIR) if (Path(BACKUP_DIR) / f).is_file()]
    all_timestamps = []

    for backup in all_backups:
        backup_timestamp = backup.split(BACKUP_FILENAME_POSTFIX)[0]
        try:
            backup_timestamp = float(backup_timestamp)
            all_timestamps.append(backup_timestamp)
        except ValueError:
            continue

    make_backup(time.time())
    all_timestamps.sort()
    timestamps_to_delete_count = len(all_timestamps) - BACKUP_MAX_COUNT + 1
    timestamps_to_delete_count = 0 if timestamps_to_delete_count < 0 else timestamps_to_delete_count
    for i in range(timestamps_to_delete_count):
        os.remove(f"{BACKUP_DIR}/{all_timestamps[i]}{BACKUP_FILENAME_POSTFIX}")
