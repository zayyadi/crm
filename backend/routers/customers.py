from fastapi import APIRouter, HTTPException, status
from app.schemas.schemas import CustomerCreate, CustomerRead
from app.models.models import Customer
from typing import List

router = APIRouter()

@router.post("/customers/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
async def create_customer(customer: CustomerCreate):
    try:
        db_customer = await Customer.create(**customer.dict())
        return db_customer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/customers/", response_model=List[CustomerRead])
async def read_customers(skip: int = 0, limit: int = 100):
    try:
        customers = await Customer.all_users()
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customers/{customer_id}", response_model=CustomerRead)
async def read_customer(customer_id: str):
    try:
        customer = await Customer.get_id(customer_id)
        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/customers/{customer_id}", response_model=CustomerRead)
async def update_customer(customer_id: str, customer: CustomerCreate):
    try:
        # First check if customer exists
        existing_customer = await Customer.get_id(customer_id)
        if existing_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        updated_customer = await Customer.update(customer_id, **customer.dict())
        # Get the updated customer to return
        customer = await Customer.get_id(customer_id)
        return customer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: str):
    try:
        # First check if customer exists
        customer = await Customer.get_id(customer_id)
        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        result = await Customer.delete(customer_id)
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
