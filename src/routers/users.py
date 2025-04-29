from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead)
def create_user(request: schemas.UserWrite, db: Session = Depends(get_db)):
    if crud.get_user_by_name(db=db, username=request.name):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f'User with name {request.name} already exists.'
        )
    
    if crud.get_user_by_email(db=db, email=request.email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f'User with email {request.email} already exists.'
        )

    return crud.create_user(db=db, request=request)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserRead)
def read_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, id=id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User id {id} not found.'
        )
    
    return user


# @router.get('/{username}', status_code=status.HTTP_200_OK, response_model=schemas.UserRead)
# def read_user_by_name(username: str, db: Session = Depends(get_db)):
#     return crud.get_user_by_name(db=db, username=username)

