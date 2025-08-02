from models.models import Customer, Contact
from schemas.schemas import CustomerCreate, ContactCreate



async def create_customer(customer: CustomerCreate):
    customer = Customer.create(**customer.dict())
    return customer

async def get_customers(skip=0, limit=100):
    gets = Customer.all_users()
    return gets


async def create_contact(contact: ContactCreate):
    contact = Contact.create(**contact.dict())
    return contact


async def get_contacts(skip=0, limit=100):
    gets = Contact.all_contacts()
    return gets

async def get_contact(contact_id: int):
    gets = Contact.get_id(contact_id)
    return gets

async def delete_contact(contact_id: int):
    gets = Contact.delete(contact_id)
    return gets