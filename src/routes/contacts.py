from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse], name="Return all contacts")
async def get_contacts(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, name="Return contact by id")
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/search_by_lastname/{contact_lastname}", response_model=List[ContactResponse], name="Return contact by lastname")
async def get_contact_by_lastname(lastname: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contact_by_lastname(lastname, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/search_by_firstname/{contact_firstname}", response_model=List[ContactResponse], name="Return contact by firstname")
async def get_contact_by_firstname(firstname: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contact_by_firstname(firstname, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/next_week_birthday/", response_model=List[ContactResponse], name="Return all contacts who have birthday next 7 days")
async def get_contacts(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_next_week_birthday_contacts(db)
    return contacts


@router.post("/", response_model=ContactResponse, name="Create contact", status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')
    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", name="Update contact by id", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", name="Delete contact by id", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
