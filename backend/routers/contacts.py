from fastapi import APIRouter, HTTPException, status
from app.schemas.schemas import ContactCreate, ContactRead
from app.models.models import Contact
from typing import List

router = APIRouter()

@router.post("/contacts/", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate):
    try:
        db_contact = await Contact.create(**contact.dict())
        return db_contact
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/contacts/", response_model=List[ContactRead])
async def get_contacts(skip: int = 0, limit: int = 100):
    try:
        contacts = await Contact.all_contacts()
        return contacts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contacts/{contact_id}", response_model=ContactRead)
async def get_contact(contact_id: int):
    try:
        contact = await Contact.get_id(contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/contacts/{contact_id}", response_model=ContactRead)
async def update_contact(contact_id: int, contact: ContactCreate):
    try:
        # First check if contact exists
        existing_contact = await Contact.get_id(contact_id)
        if existing_contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        await Contact.update(contact_id, **contact.dict())
        # Get the updated contact to return
        updated_contact = await Contact.get_id(contact_id)
        return updated_contact
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int):
    try:
        # First check if contact exists
        contact = await Contact.get_id(contact_id)
        if contact is None:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        result = await Contact.delete(contact_id)
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
