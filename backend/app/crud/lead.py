from app.models.models import Lead
from app.schemas.schemas import LeadCreate



async def create_lead(lead: LeadCreate):
    lead = Lead.create(**lead.dict())
    return lead
    

async def get_leads(skip=0, limit=100):
    gets = Lead.all_leads()
    return gets


async def get_lead(lead_id: int):
    gets = Lead.get_id(lead_id)
    return gets