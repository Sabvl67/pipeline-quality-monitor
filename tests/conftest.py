import pytest
from sqlalchemy import create_engine, text


@pytest.fixture
def connection():
    """An in-memory SQLite connection with an 'orders' table.

    10 rows, 2 of which have a NULL customer_id (null rate = 0.2).
    """
    engine = create_engine("sqlite://")
    conn = engine.connect()

    conn.execute(text("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER)"))
    conn.execute(text("""
        INSERT INTO orders (customer_id) VALUES
        (1), (2), (3), (4), (5), (6), (7), (8), (NULL), (NULL)
    """))
    conn.commit()

    yield conn

    conn.close()
