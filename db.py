import psycopg2
import psycopg2.extras

# Create a connection
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        database="todos",
        user="postgres",
        password="secret"
    )

# Initialize database using init.sql
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    with open("init.sql", "r") as f:
        cur.execute(f.read())

    conn.commit()
    conn.close()
    print("Database initialized!")

# Fetch all rows (SELECT)
def fetch_all(query, params=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows

# Execute INSERT / UPDATE / DELETE queries
def execute_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

# Allow running python db.py to initialize manually
if __name__ == "__main__":
    init_db()
