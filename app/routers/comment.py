from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas

router = APIRouter(prefix="/comment", tags=["Comment"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    check = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not check:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {comment.post_id} does not exist",
        )

    comment = models.Comments(user_id=current_user.id, **comment.dict())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    print(comment)
    return comment
