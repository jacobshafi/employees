-- Create table for time off request categories
CREATE TABLE IF NOT EXISTS request_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Create table for time off requests
CREATE TABLE IF NOT EXISTS time_off_request (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_category_id INTEGER NOT NULL,
    employee_id TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    FOREIGN KEY (request_category_id) REFERENCES request_category(id)
);

INSERT OR IGNORE INTO request_category (name) VALUES
    ('Annual Leave'),
    ('Sick Leave'),
    ('Work Remotely');