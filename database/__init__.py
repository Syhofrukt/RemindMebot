import sqlite3
from typing import Iterator
from contextlib import contextmanager
from .table_handling import TableHandler

table_handler = TableHandler()


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect("db.db")
    yield conn
    conn.commit()