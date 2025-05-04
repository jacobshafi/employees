# setup_db.py

import sqlite3
from utils.db_utils import create_all_tables

def setup_database(*, db_name: str) -> None:
    db_path = f"{db_name}.db"
    with sqlite3.connect(db_path) as conn:
        create_all_tables(conn, db_name=db_name)
    print(f"Initialized {db_name}.db using schemas/{db_name}.sql")

if __name__ == "__main__":
    setup_database(db_name="employees")
    setup_database(db_name="time_off")
    setup_database(db_name="time_off_requests")