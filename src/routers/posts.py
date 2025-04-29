from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db
from ..security import get_current_user


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


def validate_request(db: Session, post_id: int, user_id: int):
    post = crud.get_post(db, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post id {post_id} not found.'
        )
    
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'User is not a creator of post {post_id}.'
        )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostWrite)
def create_post(
    request: schemas.PostBase, 
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(get_current_user)
):
    request = schemas.PostWrite(
        title=request.title,
        content=request.content,
        user_id=current_user.id
    )

    return crud.create_post(db, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_post(
    id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(get_current_user)
):
    validate_request(db, id, current_user.id)   
     
    response = crud.remove_post(db, id)
    crud.remove_all_reactions_for_post(db, id)

    return response


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(
    id: int, 
    request: schemas.PostBase, 
    db: Session = Depends(get_db),    
    current_user: schemas.UserRead = Depends(get_current_user)
):  
    validate_request(db, id, current_user.id)    
    return crud.update_post(db, id, request)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.PostRead])
def update_post(
    skip: int | None = 0,
    limit: int | None = 100,
    db: Session = Depends(get_db)
):
    return crud.get_post_all(db=db, skip=skip, limit=limit)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostRead)
def update_post(id: int, db: Session = Depends(get_db)):
    return crud.get_post(db, id)

