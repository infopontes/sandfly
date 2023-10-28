from pydantic import BaseModel, ConfigDict, EmailStr, UUID4

from sandfly.models import ContactType, UserProfile


class UserSchema(BaseModel):
    id: UUID4
    #id: int
    username: str
    email: EmailStr
    password: str
    profile: UserProfile


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class UserDB(UserSchema):
    id: UUID4
    #id: int


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# Model of contact information


class ContactSchema(BaseModel):
    id: UUID4
    #id: int
    type_contact: ContactType
    description: str


class ContactPublic(BaseModel):
    type_contact: ContactType
    description: str


class ContactList(BaseModel):
    contacts: list[ContactPublic]


class ContactUpdate(BaseModel):
    type_contact: str | None = None
    description: str | None = None
