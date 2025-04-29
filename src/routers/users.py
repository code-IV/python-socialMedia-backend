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
    return crud.create_user(db, request)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserRead)
def read_user(id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, id)


# @router.get('/{username}', status_code=status.HTTP_200_OK, response_model=schemas.UserRead)
# def read_user_by_name(username: str, db: Session = Depends(get_db)):
#     return crud.get_user_by_name(db, username)

