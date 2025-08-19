from fastapi import APIRouter
from routers import users, customers, contacts, leads, opportunities, billing, chatbot

router = APIRouter()

# router.include_router(auth.router)
router.include_router(users.router, tags=["authentication"])
router.include_router(customers.router, prefix="/customers", tags=["customers"])
router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
router.include_router(leads.router, prefix="/leads", tags=["leads"])
router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])
router.include_router(billing.router, prefix="/billing", tags=["billing"])
router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
