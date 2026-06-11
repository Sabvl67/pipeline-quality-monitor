"""Create a local SQLite database with sample data for manually running the engine."""

from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///test.db")

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS orders"))
    conn.execute(text("CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER)"))
    conn.execute(text("""
        INSERT INTO orders (customer_id) VALUES
        (1), (2), (3), (4), (5), (6), (7), (8), (NULL), (NULL)
    """))
    conn.commit()

print("Created test.db with 'orders' table (10 rows, 2 NULL customer_ids)")
