from fastapi import APIRouter, HTTPException, status
from app.schemas.schemas import LeadCreate, LeadRead
from app.models.models import Lead
from typing import List

router = APIRouter()

@router.post("/leads/", response_model=LeadRead, status_code=status.HTTP_201_CREATED)
async def create_lead(lead: LeadCreate):
    try:
        db_lead = await Lead.create(**lead.dict())
        return db_lead
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/leads/", response_model=List[LeadRead])
async def get_leads(skip: int = 0, limit: int = 100):
    try:
        leads = await Lead.all_leads()
        return leads
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leads/{lead_id}", response_model=LeadRead)
async def get_lead(lead_id: int):
    try:
        lead = await Lead.get_id(lead_id)
        if lead is None:
            raise HTTPException(status_code=404, detail="Lead not found")
        return lead
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/leads/{lead_id}", response_model=LeadRead)
async def update_lead(lead_id: int, lead: LeadCreate):
    try:
        # First check if lead exists
        existing_lead = await Lead.get_id(lead_id)
        if existing_lead is None:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        await Lead.update(lead_id, **lead.dict())
        # Get the updated lead to return
        updated_lead = await Lead.get_id(lead_id)
        return updated_lead
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/leads/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(lead_id: int):
    try:
        # First check if lead exists
        lead = await Lead.get_id(lead_id)
        if lead is None:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        result = await Lead.delete(lead_id)
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
