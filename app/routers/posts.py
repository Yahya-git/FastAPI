from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

@router.get("/", response_model = List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    return posts

@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # post_dict = new_post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO posts (title, content, publish) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**new_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    return new_post

@router.get("/{id}", response_model = schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"message": f"post with id: {id} not found"}
    return post

@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, publish =%s WHERE id = %s RETURNING * """, (post.title, post.content, post.publish, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    post1 = updated_post.first()
    if post1 == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    updated_post.update(post.dict(), synchronize_session = False)
    db.commit() 
    return updated_post.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    deleted_post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)