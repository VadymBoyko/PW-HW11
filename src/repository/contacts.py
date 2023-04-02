from datetime import datetime, timedelta

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_next_week_birthday_contacts(db: Session):
    today = datetime.today()
    next_week = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        and_(
            func.to_char(Contact.birthday, 'MM-DD') >= func.to_char(today, 'MM-DD'),
            func.to_char(Contact.birthday, 'MM-DD') <= func.to_char(next_week, 'MM-DD')
        )
    ).all()
    return contacts


async def get_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter(Contact.email.ilike(email)).first()
    return contact


async def get_contact_by_firstname(firstname: str, db: Session):
    contacts = db.query(Contact).filter(Contact.firstname.ilike(firstname)).all()
    return contacts


async def get_contact_by_lastname(lastname: str, db: Session):
    contacts = db.query(Contact).filter(Contact.lastname.ilike(lastname)).all()
    return contacts


async def create(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        contact.notes = body.notes
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
