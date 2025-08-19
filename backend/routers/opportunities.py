from fastapi import APIRouter, HTTPException, status
from app.schemas.schemas import OpportunityCreate, OpportunityRead
from app.models.models import Opportunity
from typing import List

router = APIRouter()

@router.post("/opportunities/", response_model=OpportunityRead, status_code=status.HTTP_201_CREATED)
async def create_opportunity(opportunity: OpportunityCreate):
    try:
        db_opportunity = await Opportunity.create(**opportunity.dict())
        return db_opportunity
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/opportunities/", response_model=List[OpportunityRead])
async def get_opportunities(skip: int = 0, limit: int = 100):
    try:
        opportunities = await Opportunity.all_opportunities()
        return opportunities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/opportunities/{opportunity_id}", response_model=OpportunityRead)
async def get_opportunity(opportunity_id: int):
    try:
        opportunity = await Opportunity.get_id(opportunity_id)
        if opportunity is None:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        return opportunity
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/opportunities/{opportunity_id}", response_model=OpportunityRead)
async def update_opportunity(opportunity_id: int, opportunity: OpportunityCreate):
    try:
        # First check if opportunity exists
        existing_opportunity = await Opportunity.get_id(opportunity_id)
        if existing_opportunity is None:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        
        await Opportunity.update(opportunity_id, **opportunity.dict())
        # Get the updated opportunity to return
        updated_opportunity = await Opportunity.get_id(opportunity_id)
        return updated_opportunity
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/opportunities/{opportunity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_opportunity(opportunity_id: int):
    try:
        # First check if opportunity exists
        opportunity = await Opportunity.get_id(opportunity_id)
        if opportunity is None:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        
        result = await Opportunity.delete(opportunity_id)
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
