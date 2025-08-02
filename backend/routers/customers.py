from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.schemas import CustomerCreate, CustomerRead
import backend.app.crud.users as users
from typing import List

router = APIRouter()

@router.post("/customers/", response_model=CustomerRead)
async def create_customer(customer: CustomerCreate, db: AsyncSession = Depends(get_db)):
    return await users.create_customer(db, customer)

@router.get("/customers/", response_model=List[CustomerRead])
async def read_customers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await users.get_customers(db, skip=skip, limit=limit)
