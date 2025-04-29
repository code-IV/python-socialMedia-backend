from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, security
from ..database import get_db


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(
    request: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_name(db, request.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect credentials'
        )
    
    if not security.verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect credentials'
        )
    
    access_token = security.create_access_token(
        data={'sub': user.name}
    )
    return {'access_token': access_token, 'token_type': 'bearer'}