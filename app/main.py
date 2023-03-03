from ast import While
from cgi import test
from hashlib import new
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from . import schemas
from . import utils
from .database import engine, get_db
from .routers import posts, users, auth

# TESTING

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:

    try:
        conn = psycopg2.connect(
            "host=localhost dbname=fastapi user=emumba password=emumba", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection succesful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(5)

my_posts = [{"title": "a", "content": "b", "id": 1},
            {"title": "c", "content": "d", "id": 2}]


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
