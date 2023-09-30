from sqlalchemy import select
from sqlalchemy.orm import Session

from sandfly.models import Contact, User


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


def test_create_contact(session: Session, user: User):
    contact = Contact(
        type_contact='email',
        description='infopontes@gmail.com',
        user_id=user.id,
    )

    session.add(contact)
    session.commit()
    session.refresh(contact)

    user = session.scalar(select(User).where(User.id == user.id))

    assert contact in user.contacts
