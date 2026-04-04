import os
from pathlib import Path


def _upsert_line(lines: list[str], key: str, value: str) -> list[str]:
    prefix = f"{key}="
    replaced = False
    updated: list[str] = []
    for line in lines:
        if line.startswith(prefix):
            updated.append(f"{prefix}{value}")
            replaced = True
        else:
            updated.append(line)
    if not replaced:
        updated.append(f"{prefix}{value}")
    return updated


def main() -> None:
    neon_url = os.getenv("NEON_DATABASE_URL", "").strip()
    if not neon_url:
        raise SystemExit("Defina NEON_DATABASE_URL antes de executar este script.")

    if neon_url.startswith("postgresql://"):
        neon_url = neon_url.replace("postgresql://", "postgresql+psycopg://", 1)
    elif neon_url.startswith("postgres://"):
        neon_url = neon_url.replace("postgres://", "postgresql+psycopg://", 1)

    backend_dir = Path(__file__).resolve().parents[1]
    env_path = backend_dir / ".env"
    lines = []
    if env_path.exists():
        lines = env_path.read_text(encoding="utf-8").splitlines()

    lines = _upsert_line(lines, "DATABASE_URL", neon_url)
    lines = _upsert_line(lines, "DB_SSL_MODE", "require")
    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Arquivo atualizado: {env_path}")
    print("DATABASE_URL e DB_SSL_MODE configurados para Neon.")


if __name__ == "__main__":
    main()
