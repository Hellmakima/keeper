# sample migration file for calendar plugin

def create_tables(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS my_plugin_table (
        id INTEGER PRIMARY KEY,
        data TEXT
    )
    """)

def drop_tables(conn):
    conn.execute("DROP TABLE IF EXISTS my_plugin_table")