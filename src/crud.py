from sqlalchemy.orm import Session
from fastapi import status, HTTPException

from . import schemas, models
from .security import get_password_hash


#region User

def create_user(db: Session, request: schemas.UserWrite):
    hashed_password = get_password_hash(request.password)
    new_user=models.User(
        name=request.name,
        email=request.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

    
def get_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()
    

def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.name == username).first() 


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

#endregion

#region Post

def create_post(db: Session, request: schemas.PostWrite):
    new_post = models.Post(
        title=request.title,
        content=request.content,
        user_id=request.user_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def update_post(db: Session, id: int, request: schemas.PostWrite):
    post = db.query(models.Post).filter(models.Post.id == id)    
    post.update(request.model_dump())
    db.commit()

    return f'Post with id {id} updated.'



def remove_post(db: Session, id: int):
    post = db.query(models.Post).filter(models.Post.id == id)    
    post.delete(synchronize_session=False)
    db.commit()

    return f'Post with id {id} removed.'


def get_post(db: Session, id: int):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post id {id} not found.'
        )
    
    return post


def get_post_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


#endregion

#region Reaction

def create_reaction(db: Session, request: schemas.ReactionWrite):
    new_reaction = models.Reaction(
        is_like=request.is_like,
        user_id=request.user_id,
        post_id=request.post_id
    )

    db.add(new_reaction)
    db.commit()
    db.refresh(new_reaction)
    
    return new_reaction


def update_reaction(
    db: Session, 
    post_id: int,
    user_id: int, 
    request: schemas.ReactionUpdate
):
    reaction = db.query(models.Reaction).filter(models.Reaction.user_id == user_id, models.Reaction.post_id == post_id)
    
    if not reaction.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Reaction id {id} not found.'
        )
        
    reaction.update(request.model_dump())
    db.commit()

    return 'reaction updated'


def remove_reaction(
    db: Session,
    user_id: int,
    post_id: int
):
    reaction = db.query(models.Reaction).filter(models.Reaction.user_id == user_id, models.Reaction.post_id == post_id)
    
    if not reaction.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Reaction id {id} not found.'
        )
        
    reaction.delete()
    db.commit()

    return 'reaction deleted'


def remove_all_reactions_for_post(db: Session, post_id: int):
    reactions = db.query(models.Reaction).filter(models.Reaction.post_id == post_id)

    reactions.delete()
    db.commit()

    return 'reactions deleted'


def get_reaction(db: Session, post_id: int, user_id: int):
    return db.query(models.Reaction).filter(models.Reaction.user_id == user_id, models.Reaction.post_id == post_id).first()
    
#endregion