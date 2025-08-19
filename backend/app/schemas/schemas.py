from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Union
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    sales = "sales"
    support = "support"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole = UserRole.sales

class UserUpdate(UserBase):
    pass

    class Config:
        from_attributes = True


class UserUpdateOut(UserBase):
    pass

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str
    is_active: bool
    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: str
    class Config:
        from_attributes = True

class ContactBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class ContactCreate(ContactBase):
    customer_id: str

class ContactRead(ContactBase):
    id: int
    customer_id: int
    class Config:
        from_attributes = True

class LeadBase(BaseModel):
    name: str
    status: Optional[str] = None
    score: Optional[int] = 0

class LeadCreate(LeadBase):
    customer_id: str

class LeadRead(LeadBase):
    id: int
    customer_id: int
    class Config:
        from_attributes = True

class OpportunityBase(BaseModel):
    name: str
    value: Optional[int] = 0
    stage: Optional[str] = None

class OpportunityCreate(OpportunityBase):
    customer_id: str

class OpportunityRead(OpportunityBase):
    id: int
    customer_id: int
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    message: str
    data: dict
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class Status(BaseModel):
    message: str


class PasswordReset(BaseModel):
    password: str


# Invoicing and Billing Schemas
class InvoiceBase(BaseModel):
    customer_id: str
    amount: int
    currency: str = "USD"
    status: str = "draft"
    due_date: datetime
    description: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceRead(InvoiceBase):
    id: str
    issued_date: datetime
    
    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    invoice_id: str
    amount: int
    currency: str = "USD"
    payment_method: str
    status: str = "pending"
    transaction_id: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    id: str
    payment_date: datetime
    
    class Config:
        from_attributes = True


class SubscriptionBase(BaseModel):
    customer_id: str
    plan_name: str
    amount: int
    currency: str = "USD"
    status: str = "active"
    end_date: Optional[datetime] = None
    billing_cycle: str


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionRead(SubscriptionBase):
    id: str
    start_date: datetime
    
    class Config:
        from_attributes = True


# AI Chatbot Schemas
class ChatMessage(BaseModel):
    message: str
    sender: str  # "user" or "bot"


class ChatResponse(BaseModel):
    response: str
    suggestions: Optional[list[str]] = None


class ChatSession(BaseModel):
    session_id: str
    customer_id: Optional[str] = None
    messages: list[ChatMessage] = []


class ChatSessionCreate(BaseModel):
    customer_id: Optional[str] = None


class ChatSessionRead(ChatSession):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
