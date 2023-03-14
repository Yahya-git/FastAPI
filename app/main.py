from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, comment, like, posts, users

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(like.router)
app.include_router(comment.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
