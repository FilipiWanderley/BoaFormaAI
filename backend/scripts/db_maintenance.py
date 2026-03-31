import argparse
import shutil
from pathlib import Path
from urllib.parse import urlparse

from app.config import settings


def _sqlite_file_from_url(database_url: str) -> Path:
    if not database_url.startswith("sqlite:///"):
        raise ValueError("Operação disponível apenas para SQLite.")
    parsed = urlparse(database_url)
    db_path = parsed.path or database_url.replace("sqlite:///", "", 1)
    return Path(db_path).resolve()


def backup_sqlite(output_path: str) -> Path:
    source = _sqlite_file_from_url(settings.database_url)
    target = Path(output_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def restore_sqlite(input_path: str) -> Path:
    source = Path(input_path).resolve()
    if not source.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {source}")
    target = _sqlite_file_from_url(settings.database_url)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(prog="db_maintenance")
    subparsers = parser.add_subparsers(dest="command", required=True)

    backup_parser = subparsers.add_parser("backup")
    backup_parser.add_argument("--output", required=True)

    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument("--input", required=True)

    args = parser.parse_args()

    if args.command == "backup":
        output = backup_sqlite(args.output)
        print(f"Backup criado: {output}")
        return

    restored = restore_sqlite(args.input)
    print(f"Banco restaurado em: {restored}")


if __name__ == "__main__":
    main()
