from settings import *
import psycopg2
from models import Products
async def home_page():
    cur.execute("""SELECT * FROM products""")
    data = cur.fetchall()
    formatted_photos = []
    for prods in data:
        formatted_photos.append(
            Products(id=prods[0], post_date=prods[1], pr_name=prods[2], description=prods[3], price=prods[4],
                     photo=prods[5], photo_name=prods[6]))
    conn.commit()
    return formatted_photos