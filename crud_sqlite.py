from database import get_conn

def create_product(p):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    INSERT INTO products (nombre, descripcion, precio, stock, categoria)
    VALUES (?, ?, ?, ?, ?)
    """, (p["nombre"], p["descripcion"], p["precio"], p["stock"], p["categoria"]))

    conn.commit()
    conn.close()


def get_all():
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM products")
    rows = c.fetchall()

    conn.close()
    return rows


def delete_product(id_):
    conn = get_conn()
    c = conn.cursor()

    c.execute("DELETE FROM products WHERE id=?", (id_,))

    conn.commit()
    conn.close()


def update_stock(id_, stock):
    conn = get_conn()
    c = conn.cursor()

    c.execute("UPDATE products SET stock=? WHERE id=?", (stock, id_))

    conn.commit()
    conn.close()
