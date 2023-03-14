from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = db.query(models.Post, func.count(models.Likes.post_id).label("likes")).join(
    #     models.Likes, models.Likes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = (
    #     db.query(
    #         models.Post,
    #         func.count(distinct(models.Likes.user_id)).label("likes"),
    #         func.count(distinct(models.Comments.id)).label("comments"),
    #         func.array_agg(
    #             distinct(
    #                 cast(models.Comments.id, String) + ":" + models.Comments.comment
    #             )
    #         ).label("all_comments"),
    #     )
    #     .join(models.User, models.Post.user_id == models.User.id, isouter=True)
    #     .join(models.Likes, models.Post.id == models.Likes.post_id, isouter=True)
    #     .join(models.Comments, models.Post.id == models.Comments.post_id, isouter=True)
    #     .group_by(models.Post.id)
    #     .order_by(models.Post.id)
    #     .all()
    # )
    # subquery = (
    #     db.query(
    #         models.Comments.post_id,
    #         func.count().label("comments"),
    #         func.array_agg(models.Comments.comment).label("comment"),
    #     )
    #     .group_by(models.Comments.post_id)
    #     .subquery()
    # )

    # c = aliased(subquery)

    # posts = (
    #     db.query(
    #         models.Post,
    #         func.count(distinct(models.Likes.user_id)).label("likes"),
    #         c.c.comments,
    #         c.c.comment,
    #     )
    #     .outerjoin(c, models.Post.id == c.c.post_id)
    #     .outerjoin(models.Likes, models.Post.id == models.Likes.post_id)
    #     .group_by(models.Post.id, c.c.comments, c.c.comment)
    # ).all()
    subquery_comments = (
        db.query(
            models.Comments.post_id,
            func.count(models.Comments.id).label("num_comments"),
            func.array_agg(models.Comments.comment).label("comments"),
            func.array_agg(models.User.email).label("comment_emails"),
        )
        .join(models.User, models.Comments.user_id == models.User.id)
        .group_by(models.Comments.post_id)
        .subquery()
    )

    posts = (
        db.query(
            models.Post,
            func.count(models.Likes.user_id).label("num_likes"),
            subquery_comments.c.num_comments,
            subquery_comments.c.comments,
            subquery_comments.c.comment_emails,
        )
        .outerjoin(subquery_comments, models.Post.id == subquery_comments.c.post_id)
        .outerjoin(models.Likes, models.Post.id == models.Likes.post_id)
        .group_by(
            models.Post.id,
            subquery_comments.c.num_comments,
            subquery_comments.c.comments,
            subquery_comments.c.comment_emails,
        )
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
    ).all()
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    new_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # post_dict = new_post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO posts (title, content, publish) VALUES (%s, %s, %s) RETURNING * """, (new_post.title, new_post.content, new_post.publish))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(user_id=current_user.id, **new_post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = (
    #     db.query(models.Post, func.count(models.Likes.post_id).label("num_likes"))
    #     .join(models.Likes, models.Likes.post_id == models.Post.id, isouter=True)
    #     .group_by(models.Post.id)
    #     .filter(models.Post.id == id)
    #     .first()
    # )
    subquery_comments = (
        db.query(
            models.Comments.post_id,
            func.count(models.Comments.id).label("num_comments"),
            func.array_agg(models.Comments.comment).label("comments"),
            func.array_agg(models.User.email).label("comment_emails"),
        )
        .join(models.User, models.Comments.user_id == models.User.id)
        .group_by(models.Comments.post_id)
        .subquery()
    )

    post = (
        (
            db.query(
                models.Post,
                func.count(models.Likes.user_id).label("num_likes"),
                subquery_comments.c.num_comments,
                subquery_comments.c.comments,
                subquery_comments.c.comment_emails,
            )
            .outerjoin(subquery_comments, models.Post.id == subquery_comments.c.post_id)
            .outerjoin(models.Likes, models.Post.id == models.Likes.post_id)
            .group_by(
                models.Post.id,
                subquery_comments.c.num_comments,
                subquery_comments.c.comments,
                subquery_comments.c.comment_emails,
            )
        )
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{"message": f"post with id: {id} not found"}
    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, publish =%s WHERE id = %s RETURNING * """, (post.title, post.content, post.publish, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    if updated_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'{"not authorize to perform requested action"}',
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    if deleted_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'{"not authorize to perform requested action"}',
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
