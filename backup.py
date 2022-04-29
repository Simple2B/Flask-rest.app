import os
import sys
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
BACKUP_FILENAME_POSTFIX = ".dump"


def make_backup(filename):
    dump_cmd = f"pg_dump -U {DB_USER} -F c {DB_NAME} > /db_dump/{filename}{BACKUP_FILENAME_POSTFIX};"
    docker_cmd = f"docker-compose exec db bash -c '{dump_cmd}'"
    os.system(f"{docker_cmd}")


def restore_from_backup(filename):
    dump_cmd = f"pg_restore -U {DB_USER} -d {DB_NAME} /db_dump/{filename}{BACKUP_FILENAME_POSTFIX};"
    docker_cmd = f"docker-compose exec db bash -c '{dump_cmd}'"
    os.system(f"{docker_cmd}")


def main():
    if len(sys.argv) < 2:
        return

    make_backup(sys.argv[1])


if __name__ == "__main__":
    main()
