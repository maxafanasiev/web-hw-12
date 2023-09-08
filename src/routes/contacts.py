from typing import List

from fastapi import Depends, Query, APIRouter, status
from sqlalchemy.orm import Session

from src.db.models import User
from src.schemas import ContactRequest, ContactResponse
from src.db.db_connect import get_db
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactRequest, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create_contact(contact, db, current_user)
    return contact


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, db, current_user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, db, current_user)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, updated_contact: ContactRequest,
                         db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, updated_contact, db, current_user)
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.delete_contact(contact_id, db, current_user)
    return contact


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
        q: str = Query(..., description="Search query for name, last name, or email"),
        skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
):
    contacts = await repository_contacts.search_contacts(q, skip, limit, db, current_user)
    return contacts


@router.get("/birthdays/", response_model=List[ContactResponse])
async def upcoming_birthdays(db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    upcoming_birthdays_this_year = await repository_contacts.upcoming_birthdays(db, current_user)
    return upcoming_birthdays_this_year
