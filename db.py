import mysql.connector
import config

def q(sql, params=(), one=False, commit=False):
    """Run one SQL query. Returns rows (list of dicts), one row, or the new row id."""
    conn = mysql.connector.connect(host=config.DB_HOST, user=config.DB_USER,
                                   password=config.DB_PASSWORD, database=config.DB_NAME)
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, params)
        if commit:
            conn.commit()
            return cur.lastrowid
        rows = cur.fetchall()
        return (rows[0] if rows else None) if one else rows
    finally:
        cur.close()
        conn.close()
