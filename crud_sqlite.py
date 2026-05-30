from database import get_db

def create_product(p):

    db = get_db()

    db.table("products").insert({
        "nombre": p["nombre"],
        "descripcion": p["descripcion"],
        "precio": float(p["precio"]),
        "stock": int(p["stock"]),
        "categoria": p["categoria"]
    }).execute()


def get_all():

    db = get_db()

    result = db.table("products").select("*").execute()

    rows = []

    for r in result.data:
        rows.append((
            r["id"],
            r["nombre"],
            r["descripcion"],
            r["precio"],
            r["stock"],
            r["categoria"]
        ))

    return rows


def update_stock(id_, stock):

    db = get_db()

    db.table("products").update({
        "stock": int(stock)
    }).eq("id", id_).execute()


def delete_product(id_):

    db = get_db()

    db.table("products").delete().eq("id", id_).execute()
