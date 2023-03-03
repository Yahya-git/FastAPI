from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth, like

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(like.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
