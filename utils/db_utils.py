import os
import sqlite3

SCHEMA_FOLDER = os.path.join(os.path.dirname(__file__), "schemas")

def create_all_tables(conn: sqlite3.Connection, *, db_name: str) -> None:
    """
    Applies the SQL script corresponding to the given db_name.
    For example: 'employees' will load schemas/employees.sql.
    """
    schema_file = os.path.join(SCHEMA_FOLDER, f"{db_name}.sql")
    
    if not os.path.isfile(schema_file):
        raise FileNotFoundError(f"No schema found for database '{db_name}' at {schema_file}")
    
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with conn:
        conn.executescript(schema_sql)