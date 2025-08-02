from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.schemas import OpportunityCreate, OpportunityRead
import backend.app.crud.users as users
from typing import List

router = APIRouter()

@router.post("/opportunities/", response_model=OpportunityRead)
async def create_opportunity(opportunity: OpportunityCreate, db: AsyncSession = Depends(get_db)):
    return await users.create_opportunity(db, opportunity)

@router.get("/opportunities/", response_model=List[OpportunityRead])
async def read_opportunities(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await users.get_opportunities(db, skip=skip, limit=limit)

@router.get("/opportunities/{opportunity_id}", response_model=OpportunityRead)
async def read_opportunity(opportunity_id: int, db: AsyncSession = Depends(get_db)):
    opportunity = await users.get_opportunity(db, opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opportunity
