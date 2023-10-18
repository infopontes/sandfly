from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship



class UserProfile(str, Enum):
    admin = 'administrator'
    student = 'student'
    professor = 'professor'
    research = 'research'
    basic = 'basic'
    



class ContactType(str, Enum):
    phone = 'phone'
    email = 'email'


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    profile: Mapped[UserProfile] = mapped_column(default='basic')

    contacts: Mapped[list['Contact']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )


class Contact(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(primary_key=True)
    type_contact: Mapped[ContactType]
    description: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(back_populates='contacts')
