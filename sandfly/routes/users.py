import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from sandfly.database import get_session
from sandfly.models import User
from sandfly.schemas import Message, UserList, UserPublic, UserSchema
from sandfly.security import get_current_user, get_password_hash

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserPublic, status_code=201)
def create_user(user: UserSchema, session: Session):
    db_user = session.scalar(select(User).where(User.email == user.email))
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    hashed_password = get_password_hash(user.password)

    db_user = User(
        id=user.id,
        email=user.email,
        username=user.username,
        password=hashed_password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/', response_model=UserList)
def read_users(
    session: Session,
    user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    ):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: uuid.UUID, user: UserSchema, session: Session, current_user: CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')
    
    hashed_password = get_password_hash(user.password)

    
    current_user.username = user.username
    current_user.password = hashed_password
    current_user.email = user.email
    current_user.profile = user.profile
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: uuid.UUID, session: Session, current_user: CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return {'detail': 'User deleted'}
