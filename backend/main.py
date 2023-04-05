import uvicorn
from models import Products
import boto3
from settings import *
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile


@app.get("/home", response_class=JSONResponse)
async def home_page():
    cur.execute("""SELECT * FROM products""")
    data = cur.fetchall()
    for prods in data:
        formatted_photos.append(
            Products(id=prods[0], post_date=prods[1], pr_name=prods[2], description=prods[3], price=prods[4],
                     photo=prods[5], photo_name=prods[6]))
    conn.commit()
    return formatted_photos


@app.post("/photos", status_code=201, response_model=Products)
async def add_photo(name: str, description: str, price: float, file: UploadFile = File(...)):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={"ACL": "public-read"})

    uploaded_file_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file.filename}"
    cur.execute(
        f"""INSERT INTO products (post_date, pr_name, photo, description, price, photo_name) VALUES ('{datetime.now()}', '{name}', '{uploaded_file_url}', '{description}', '{price}', '{file.filename}')""")
    conn.commit()


@app.get("/{Product_id}")
async def choose(Product_id):
    print(Product_id)
    cur.execute(f"""SELECT * FROM products WHERE id = {Product_id}git """)
    products_for = cur.fetchall()
    for prod in products_for:
        formatted_photos.append(
            Products(id=prod[0], post_date=prod[1], pr_name=prod[2], description=prod[3], price=prod[4],
                     photo=prod[5], photo_name=prod[6]))
    return formatted_photos


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
