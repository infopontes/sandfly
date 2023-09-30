from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from sandfly.database import get_session
from sandfly.models import Contact, User
from sandfly.schemas import (
    ContactList,
    ContactPublic,
    ContactSchema,
    ContactUpdate,
    Message,
)
from sandfly.security import get_current_user

CurrentUser = Annotated[User, Depends(get_current_user)]
Session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix='/contacts', tags=['contacts'])

# router = APIRouter()


@router.post('/', response_model=ContactPublic)
def create_contact(
    contact: ContactSchema, user: CurrentUser, session: Session
):
    db_contact: Contact = Contact(
        type_contact=contact.type_contact,
        description=contact.description,
        user_id=user.id,
    )
    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)

    return db_contact


@router.get('/', response_model=ContactList)
def list_contacts(
    session: Session,
    user: CurrentUser,
    type_contact: str = Query(None),
    description: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Contact).where(Contact.user_id == user.id)

    if type_contact:
        query = query.filter(Contact.type_contact == type_contact)

    if description:
        query = query.filter(Contact.description.contains(description))

    contacts = session.scalars(query.offset(offset).limit(limit)).all()

    return {'contacts': contacts}


@router.patch('/{contact_id}', response_model=ContactPublic)
def patch_contact(
    contact_id: int,
    session: Session,
    user: CurrentUser,
    contact: ContactUpdate,
):
    db_contact = session.scalar(
        select(Contact).where(
            Contact.user_id == user.id, Contact.id == contact_id
        )
    )

    if not db_contact:
        raise HTTPException(status_code=404, detail='Task not found.')

    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)

    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)

    return db_contact


@router.delete('/{contact_id}', response_model=Message)
def delete_contact(contact_id: int, session: Session, user: CurrentUser):
    contact = session.scalar(
        select(Contact).where(
            Contact.user_id == user.id, Contact.id == contact_id
        )
    )

    if not contact:
        raise HTTPException(status_code=404, detail='Task not found.')

    session.delete(contact)
    session.commit()

    return {'detail': 'Contact has been deleted successfully.'}
