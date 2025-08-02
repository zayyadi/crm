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
    id: int
    is_active: bool
    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    class Config:
        orm_mode = True

class ContactBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class ContactCreate(ContactBase):
    customer_id: int

class ContactRead(ContactBase):
    id: int
    customer_id: int
    class Config:
        orm_mode = True

class LeadBase(BaseModel):
    name: str
    status: Optional[str] = None
    score: Optional[int] = 0

class LeadCreate(LeadBase):
    customer_id: int

class LeadRead(LeadBase):
    id: int
    customer_id: int
    class Config:
        orm_mode = True

class OpportunityBase(BaseModel):
    name: str
    value: Optional[int] = 0
    stage: Optional[str] = None

class OpportunityCreate(OpportunityBase):
    customer_id: int

class OpportunityRead(OpportunityBase):
    id: int
    customer_id: int
    class Config:
        orm_mode = True

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