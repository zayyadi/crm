from schemas.schemas import OpportunityCreate
from models.models import Opportunity


async def create_opportunity(opportunity: OpportunityCreate):
    opportunity = Opportunity.create(**opportunity.dict())
    return opportunity

async def get_opportunities(skip=0, limit=100):
    get_opportunities = Opportunity.all_opportunities()
    return get_opportunities


async def get_opportunity(opportunity_id: int):
    opps = Opportunity.get_id(opportunity_id)
    return opps