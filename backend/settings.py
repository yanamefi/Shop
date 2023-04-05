import os
import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

formatted_photos = []

cur = conn.cursor()

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

