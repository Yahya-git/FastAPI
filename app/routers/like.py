from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas

router = APIRouter(prefix="/like", tags=["Like"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def like(
    like: schemas.Like,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    check = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {like.post_id} does not exist",
        )
    like_query = db.query(models.Likes).filter(
        models.Likes.post_id == like.post_id, models.Likes.user_id == current_user.id
    )
    found_like = like_query.first()
    if like.dir == 1:
        if found_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"you have already liked post: {like.post_id}",
            )
        new_like = models.Likes(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully liked post"}
    else:
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'{"like does not exist"}'
            )
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully unliked post"}
