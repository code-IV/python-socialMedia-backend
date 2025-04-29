from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db
from ..security import get_current_user


router = APIRouter(
    prefix='/reactions',
    tags=['Reactions']
)


def validate_request(db: Session, reaction_id, user_id):
    reaction = crud.get_reaction(db, reaction_id)

    if not reaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Reaction id {reaction_id} not found.'
        )
    
    if reaction.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is not creator of the reaction.'
        )
    

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ReactionRead)
def create_reaction(
    request: schemas.ReactionBase, 
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(get_current_user)
):
    post = crud.get_post(db, request.post_id)

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
    return crud.create_reaction(db, request)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_reaction(
    id: int,
    request: schemas.ReactionWrite, 
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(get_current_user)
):
    validate_request(db, id, current_user.id)
    return crud.update_reaction(db, id, request,)


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
def remove_reaction(
    id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(get_current_user)
):
    validate_request(db, id, current_user.id)
    return crud.remove_reaction(db, id)

