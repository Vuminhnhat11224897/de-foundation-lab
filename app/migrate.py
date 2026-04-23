from pathlib import Path
import psycopg
from db import DATABASE_URL


BASE_DIR = Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = BASE_DIR / "db" / "migrations"


def ensure_migrations_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(255) PRIMARY KEY,
                applied_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)
    conn.commit()


def get_applied_migrations(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT version FROM schema_migrations;")
        rows = cur.fetchall()
    return {row[0] for row in rows}


def apply_migration(conn, filepath: Path):
    version = filepath.name

    sql = filepath.read_text(encoding="utf-8")

    with conn.cursor() as cur:
        cur.execute(sql)
        cur.execute(
            "INSERT INTO schema_migrations (version) VALUES (%s);",
            (version,)
        )
    conn.commit()
    print(f"Applied: {version}")


def main():
    migration_files = sorted(MIGRATIONS_DIR.glob("*.up.sql"))

    if not migration_files:
        print(f"No migration files found in: {MIGRATIONS_DIR}")
        return

    with psycopg.connect(DATABASE_URL) as conn:
        ensure_migrations_table(conn)
        applied = get_applied_migrations(conn)

        for filepath in migration_files:
            if filepath.name not in applied:
                apply_migration(conn, filepath)


if __name__ == "__main__":
    main()