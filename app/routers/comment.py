from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models


router = APIRouter(
    prefix="/comment",
    tags=['Comment']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def comment(comment: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    check = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {comment.post_id} does not exist")
    # comment_query = db.query(models.Comment).filter(
    #     models.Comment.post_id == comment.post_id, models.Comment.user_id == current_user.id)
    # found_comment = comment_query.first()
    # if (like.dir == 1):
    #     if found_like:
    #         raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                             detail=f"user{current_user.id} has already liked post: {like.post_id}")
    comment = models.Comments(user_id = current_user.id, **comment.dict())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    print(comment)
    return comment
    # else:
    #     if not found_like:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND, detail=f"like does not exist")
    #     like_query.delete(synchronize_session=False)
    #     db.commit()
    #     return {"message": "successfully unliked post"}