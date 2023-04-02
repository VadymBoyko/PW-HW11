from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    firstname: str
    lastname: str = Field(min_length=2)
    birthday: datetime
    phone: str
    email: EmailStr
    notes: str = Field('')


class ContactResponse(BaseModel):
    id: int
    firstname: str
    lastname: str = Field(min_length=2)
    birthday: datetime
    phone: str
    email: EmailStr
    notes: str
    days_to_next_birthday: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
