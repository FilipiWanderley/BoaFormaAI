import argparse
import os
import shutil
import subprocess
from datetime import datetime, timedelta
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


def _postgres_dsn_for_cli(database_url: str) -> str:
    if not database_url.startswith("postgresql"):
        raise ValueError("Operação disponível apenas para PostgreSQL.")
    return database_url.replace("postgresql+psycopg://", "postgresql://", 1)


def _prune_old_backups(directory: Path, retention_days: int) -> int:
    if retention_days <= 0:
        return 0
    cutoff = datetime.utcnow() - timedelta(days=retention_days)
    removed = 0
    for file in directory.glob("*.dump"):
        modified = datetime.utcfromtimestamp(file.stat().st_mtime)
        if modified < cutoff:
            file.unlink(missing_ok=True)
            removed += 1
    return removed


def backup_postgres(output_dir: str, retention_days: int = 7) -> Path:
    target_dir = Path(output_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    target_file = target_dir / f"boaforma_pg_{timestamp}.dump"
    dsn = _postgres_dsn_for_cli(settings.database_url)

    env = os.environ.copy()
    env.setdefault("PGCONNECT_TIMEOUT", "10")
    subprocess.run(
        [
            "pg_dump",
            "--format=custom",
            "--no-owner",
            "--no-privileges",
            f"--file={target_file}",
            dsn,
        ],
        check=True,
        env=env,
    )
    _prune_old_backups(target_dir, retention_days)
    return target_file


def restore_postgres(input_path: str, clean: bool = True) -> Path:
    source = Path(input_path).resolve()
    if not source.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {source}")
    dsn = _postgres_dsn_for_cli(settings.database_url)
    command = [
        "pg_restore",
        "--no-owner",
        "--no-privileges",
    ]
    if clean:
        command.extend(["--clean", "--if-exists"])
    command.extend([f"--dbname={dsn}", str(source)])
    env = os.environ.copy()
    env.setdefault("PGCONNECT_TIMEOUT", "10")
    subprocess.run(command, check=True, env=env)
    return source


def main() -> None:
    parser = argparse.ArgumentParser(prog="db_maintenance")
    subparsers = parser.add_subparsers(dest="command", required=True)

    backup_parser = subparsers.add_parser("backup")
    backup_parser.add_argument("--output", required=True)
    backup_parser.add_argument("--retention-days", type=int, default=7)

    restore_parser = subparsers.add_parser("restore")
    restore_parser.add_argument("--input", required=True)
    restore_parser.add_argument("--clean", action="store_true")

    args = parser.parse_args()

    if args.command == "backup":
        if settings.database_url.startswith("sqlite:///"):
            output = backup_sqlite(args.output)
            print(f"Backup SQLite criado: {output}")
            return
        output = backup_postgres(args.output, retention_days=args.retention_days)
        print(f"Backup PostgreSQL criado: {output}")
        return

    if settings.database_url.startswith("sqlite:///"):
        restored = restore_sqlite(args.input)
        print(f"SQLite restaurado em: {restored}")
        return

    restored = restore_postgres(args.input, clean=args.clean)
    print(f"PostgreSQL restaurado usando: {restored}")


if __name__ == "__main__":
    main()
