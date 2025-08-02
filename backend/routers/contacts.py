from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.schemas import ContactCreate, ContactRead
import backend.app.crud.users as users
from typing import List

router = APIRouter()

@router.post("/contacts/", response_model=ContactRead)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await users.create_contact(db, contact)

@router.get("/contacts/", response_model=List[ContactRead])
async def read_contacts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await users.get_contacts(db, skip=skip, limit=limit)

@router.get("/contacts/{contact_id}", response_model=ContactRead)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await users.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
