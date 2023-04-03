import os
import psycopg2
import uvicorn
import boto3
from datetime import datetime
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, Response
from models import Products

os.environ['AWS_ACCESS_KEY_ID'] = 'AKIASBTY4V72VTE5V6PX'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'yPKwrszKb41CRHQycG7e3adw9g8GvNdn517mhUBK'
S3_BUCKET_NAME = "fastapi-bucket-postgresql"
conn = psycopg2.connect(
    database="exampledb",
    user="docker",
    password="postgres160708",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

formatted_date = datetime.now().strftime("%Y-%m-%d")

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/home", response_class=JSONResponse)
async def home_page():
    cur.execute("""SELECT * FROM products""")
    data = cur.fetchall()
    formatted_photos = []
    for prods in data:
        formatted_photos.append(
            Products(id=prods[0], post_date=prods[1], pr_name=prods[2], description=prods[3], price=prods[4], photo=prods[5], photo_name=prods[6]))
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


@app.get("/me")
async def me():
    cur.execute("""SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    AND table_type = 'BASE TABLE';""")
    x = cur.fetchall()
    print(x)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
