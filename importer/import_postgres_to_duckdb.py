import duckdb
import logging
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_and_attach_secret(
    conn: duckdb.DuckDBPyConnection, secret_name: str, postgres_config: Dict[str, str]
) -> None:
    """
    Creates and attaches a secret for PostgreSQL connection in DuckDB.
    """
    required_keys = {"host", "port", "database", "user", "password"}
    missing_keys = required_keys - postgres_config.keys()
    if missing_keys:
        raise ValueError(f"Missing keys in postgres_config: {', '.join(missing_keys)}")

    logging.info("Dropping existing secret (if exists)...")
    conn.execute(f"DROP SECRET IF EXISTS {secret_name};")

    logging.info("Creating new PostgreSQL secret...")
    conn.execute(
        f"""
        CREATE SECRET {secret_name} (
            TYPE POSTGRES,
            HOST '{postgres_config["host"]}',
            PORT {postgres_config["port"]},
            DATABASE '{postgres_config["database"]}',
            USER '{postgres_config["user"]}',
            PASSWORD '{postgres_config["password"]}'
        );
        """
    )

    logging.info("Attaching PostgreSQL connection using secret...")
    conn.execute(f"ATTACH '' AS postgres_db (TYPE POSTGRES, SECRET {secret_name});")
    logging.info("PostgreSQL connection attached successfully.")


def drop_all_tables(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Drops all existing tables in all schemas in the DuckDB database to ensure a clean reload.
    """
    logging.info("Fetching list of existing tables in DuckDB...")
    tables = conn.execute(
        """
        SELECT table_schema, table_name 
        FROM information_schema.tables
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog', 'duckdb_internal')
        """
    ).fetchall()

    if not tables:
        logging.info("No tables found to drop.")
        return

    for schema, table_name in tables:
        conn.execute(f'DROP TABLE IF EXISTS "{schema}"."{table_name}";')
        logging.info(f"Dropped table: {schema}.{table_name}")

    logging.info("All existing tables dropped from all schemas.")


def import_table(conn: duckdb.DuckDBPyConnection, table_name: str) -> None:
    """
    Import a table from PostgreSQL into DuckDB, ensuring atomic reload.
    """
    logging.info(f"Starting import for table: {table_name}")

    safe_table_name = f'"{table_name}"'

    logging.info(f"Dropping existing table: {table_name} (if exists)...")
    conn.execute(f"DROP TABLE IF EXISTS {safe_table_name};")

    cmd = f"""
        CREATE TABLE {safe_table_name} AS
        SELECT * FROM postgres_db.{table_name};
    """

    try:
        conn.execute(cmd)
        logging.info(f"Successfully imported table: {table_name}")
    except duckdb.Error as e:
        logging.error(f"Error importing table {table_name}: {e}")
        raise RuntimeError(f"Error importing table {table_name}: {e}")


def main() -> None:
    """
    Main function to import tables from PostgreSQL to DuckDB, ensuring atomic reload.
    """
    logging.info("Starting PostgreSQL to DuckDB import process...")

    postgres_config: Dict[str, str] = {
        "host": "poplin-postgres",
        "port": 5432,
        "database": "poplin-store",
        "user": "postgres",
        "password": "secretpassword",
    }

    duckdb_path: str = "/app/analytics.duckdb"
    secret_name: str = "postgres_secret"
    tables: List[str] = ["orders", "returns", "managers"]

    conn = duckdb.connect(duckdb_path)

    try:
        logging.info("Installing and loading DuckDB PostgreSQL extension...")
        conn.execute("INSTALL postgres;")
        conn.execute("LOAD postgres;")

        create_and_attach_secret(conn, secret_name, postgres_config)
        drop_all_tables(conn)

        for table in tables:
            import_table(conn, table)

        logging.info("Data import completed successfully.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    finally:
        logging.info("Closing DuckDB connection.")
        conn.close()


if __name__ == "__main__":
    main()
