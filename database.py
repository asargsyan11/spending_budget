import sqlite3

CREATE_SPENDINGS_TABLE = """
CREATE TABLE IF NOT EXISTS spendings (
    id INTEGER PRIMARY KEY,
    category TEXT CHECK(category IN ('Food', 'Fees', 'Entertainment', 'Transport', 'Rent', 'Others')),
    amount INTEGER,
    month TEXT CHECK(month IN ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')),
    year INTEGER
);
"""
CREATE_BUDGET_TABLE = """
CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY,
    category TEXT CHECK(category IN ('Food', 'Fees', 'Entertainment', 'Transport', 'Rent', 'Others')),
    amount INTEGER,
    month TEXT CHECK(month IN ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')),
    year INTEGER
);
"""
INSERT_SPENDING = """
INSERT INTO spendings (category, amount, month, year) VALUES (?, ?, ?, ?);
"""
INSERT_BUDGET = """
INSERT INTO budget (category, amount, month, year) VALUES (?, ?, ?, ?);
"""
GET_ALL_SPENDINGS = "SELECT * FROM spendings;"
GET_ALL_BUDGET = "SELECT * FROM budget;"
GET_SPENDINGS_BY_CATEGORY_MONTH_YEAR = """
SELECT SUM(amount) FROM spendings WHERE category = ? AND month = ? AND year = ?;
"""
GET_BUDGET_BY_CATEGORY_MONTH_YEAR = """
SELECT amount FROM budget WHERE category = ? AND month = ? AND year = ?;
"""

def connect():
    return sqlite3.connect("data.db")

def create_table(connection, create_table_sql):
    with connection:
        connection.execute(create_table_sql)

def add_record(connection, insert_sql, record):
    with connection:
        connection.execute(insert_sql, record)

def get_all_records(connection, query):
    with connection:
        return connection.execute(query).fetchall()

def get_total_spendings(connection, category, month, year):
    with connection:
        result = connection.execute(GET_SPENDINGS_BY_CATEGORY_MONTH_YEAR, (category, month, year)).fetchone()
        return result[0] if result[0] else 0

def get_budget(connection, category, month, year):
    with connection:
        result = connection.execute(GET_BUDGET_BY_CATEGORY_MONTH_YEAR, (category, month, year)).fetchone()
        return result[0] if result else None