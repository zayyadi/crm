from fastapi import APIRouter
from routers import users, customers, contacts, leads, opportunities

router = APIRouter()

# router.include_router(auth.router)
router.include_router(users.router)
router.include_router(customers.router)
router.include_router(contacts.router)
router.include_router(leads.router)
router.include_router(opportunities.router)
