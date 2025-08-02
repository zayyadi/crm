from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.schemas import LeadCreate, LeadRead
import backend.app.crud.users as users
from typing import List

router = APIRouter()

@router.post("/leads/", response_model=LeadRead)
async def create_lead(lead: LeadCreate, db: AsyncSession = Depends(get_db)):
    return await users.create_lead(db, lead)

@router.get("/leads/", response_model=List[LeadRead])
async def read_leads(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await users.get_leads(db, skip=skip, limit=limit)

@router.get("/leads/{lead_id}", response_model=LeadRead)
async def read_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    lead = await users.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
