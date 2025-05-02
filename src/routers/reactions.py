from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db
from ..security import get_current_user


router = APIRouter(
    prefix='/reactions',
    tags=['Reactions']
)


def validate_request(db: Session, post_id, user_id):
    reaction = crud.get_reaction(db, post_id, user_id)
    print(reaction)

    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Reaction not found.'
        )
    

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ReactionRead)
def create_reaction(
    request: schemas.ReactionBase, 
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(get_current_user)
):
    post = crud.get_post(db=db, id=request.post_id)

    if post.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User can not add reaction to own post.'
        )
    
    request = schemas.ReactionWrite(
        is_like=request.is_like,
        post_id=request.post_id,
        user_id=current_user.id
    )
    return crud.create_reaction(db=db, request=request)


@router.put('/{post_id}', status_code=status.HTTP_202_ACCEPTED)
def update_reaction(
    post_id: int,
    request: schemas.ReactionUpdate, 
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(get_current_user)
):
    validate_request(db=db, post_id=post_id, user_id=current_user.id)
    return crud.update_reaction(db=db, post_id=post_id, user_id=current_user.id, request=request)


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_reaction(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(get_current_user)
):
    validate_request(db=db, post_id=post_id, user_id=current_user.id)
    return crud.remove_reaction(db=db, user_id=current_user.id, post_id=post_id)
