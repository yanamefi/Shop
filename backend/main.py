import boto3
import psycopg2
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from models import Products
from typing import List


conn=psycopg2.connect(
    database="exampledb",
    user="docker",
    password="postgres160708",
    host="localhost",
    port="5432",
)
cur = conn.cursor()
app = FastAPI(debug=True)

@app.get("/home")
async def home_page(response_model=List[Products]):
    cur.execute("""SELECT * FROM Products ORDER BY id DESC""")
    data = cur.fetchall()
    formatted_photos = []
    for prods in data:
        formatted_photos.append(
            Products(
                id=prods[0],
                post_date=prods[1],
                name=prods[2],
                photo_url=prods[3],
                description=prods[4]
            )
        )
    cur.close()
    conn.close()
    return formatted_photos

@app.post("/photos", status_code=201)
async def add_photo(file: UploadFile = File(... )):
    conn.commit()
    cur.close()
    conn.close()

@app.get("/cr")
async def cr():
    cur.execute("""CREATE TABLE Products (
        id SERIAL PRIMARY KEY NOT NULL,
        post_date DATE NOT NULL,
        pr_name VARCHAR(16) NULL,
        photo BYTEA NOT NULL,
        description VARCHAR(200) NULL);
        """)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)