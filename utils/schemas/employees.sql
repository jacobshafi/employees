CREATE TABLE IF NOT EXISTS employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    email TEXT NOT NULL,
    salary REAL NOT NULL,
    created_at TEXT NOT NULL,
    modified_at TEXT NOT NULL
);