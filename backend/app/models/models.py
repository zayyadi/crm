from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum,
    Boolean,
    and_,
    func,
    DateTime,
)
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy.future import select
import enum
from uuid import uuid4

from app.core.database import Base, db


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    sales = "sales"
    support = "support"


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.sales)
    created_at = Column(
        DateTime,
        index=True,
        default=datetime.utcnow,
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        nullable=True,
        onupdate=func.current_timestamp(),
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(id={self.id}, full_name={self.full_name}, )>"
        )

    @classmethod
    async def create(cls, **kwargs):
        user = cls(id=str(uuid4()), **kwargs)
        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def update_by_email(cls, email, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.email == email)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        # return True

    @classmethod
    async def all_users(cls):
        query = select(cls)
        users = await db.execute(query)
        user = users.scalars().all()
        return user

    @classmethod
    async def get_id(cls, id):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user

    @classmethod
    async def get_email(cls, email):
        query = select(cls).where(and_(cls.email == email))
        users = await db.execute(query)
        user = users.scalars().first()
        return user

    # @classmethod
    # async def get_all(cls):
    #     query = select(cls)
    #     users = await db.execute(query)
    #     users = users.scalars().all()
    #     return users

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True

    @classmethod
    async def delete_by_email(cls, email):
        query = sqlalchemy_delete(cls).where(cls.email == email)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True


class Customer(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)
    address = Column(String)
    contacts = relationship("Contact", back_populates="customer")
    leads = relationship("Lead", back_populates="customer")
    opportunities = relationship("Opportunity", back_populates="customer")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, full_name={self.name}, )>"

    @classmethod
    async def create(cls, **kwargs):
        user = cls(id=str(uuid4()), **kwargs)
        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def update_by_email(cls, email, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.email == email)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        # return True

    @classmethod
    async def all_users(cls):
        query = select(cls)
        users = await db.execute(query)
        user = users.scalars().all()
        return user

    @classmethod
    async def get_id(cls, id):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user

    @classmethod
    async def get_email(cls, email):
        query = select(cls).where(and_(cls.email == email))
        users = await db.execute(query)
        user = users.scalars().first()
        return user

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True

    @classmethod
    async def delete_by_email(cls, email):
        query = sqlalchemy_delete(cls).where(cls.email == email)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    customer_id = Column(String, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="contacts")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, full_name={self.name}, )>"

    @classmethod
    async def create(cls, **kwargs):
        user = cls(**kwargs)
        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def update_by_email(cls, email, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.email == email)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        # return True

    @classmethod
    async def all_contacts(cls):
        query = select(cls)
        users = await db.execute(query)
        user = users.scalars().all()
        return user

    @classmethod
    async def get_id(cls, id):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user

    @classmethod
    async def get_email(cls, email):
        query = select(cls).where(and_(cls.email == email))
        users = await db.execute(query)
        user = users.scalars().first()
        return user

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True

    @classmethod
    async def delete_by_email(cls, email):
        query = sqlalchemy_delete(cls).where(cls.email == email)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True


class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String)
    score = Column(Integer, default=0)
    customer_id = Column(String, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="leads")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, full_name={self.name}, )>"

    @classmethod
    async def create(cls, **kwargs):
        user = cls(**kwargs)
        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def all_leads(cls):
        query = select(cls)
        users = await db.execute(query)
        user = users.scalars().all()
        return user

    @classmethod
    async def get_id(cls, id):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    amount = Column(Integer)  # Store in cents to avoid floating point issues
    currency = Column(String, default="USD")
    status = Column(String, default="draft")  # draft, sent, paid, overdue, cancelled
    due_date = Column(DateTime)
    issued_date = Column(DateTime, default=datetime.utcnow)
    description = Column(String)
    customer = relationship("Customer", back_populates="invoices")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, amount={self.amount}, status={self.status})>"

    @classmethod
    async def create(cls, **kwargs):
        invoice = cls(id=str(uuid4()), **kwargs)
        db.add(invoice)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return invoice

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def all_invoices(cls):
        query = select(cls)
        invoices = await db.execute(query)
        return invoices.scalars().all()

    @classmethod
    async def get_id(cls, id):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True


class Payment(Base):
    __tablename__ = "payments"
    id = Column(String, primary_key=True)
    invoice_id = Column(String, ForeignKey("invoices.id"))
    amount = Column(Integer)  # Store in cents
    currency = Column(String, default="USD")
    payment_method = Column(String)  # credit_card, bank_transfer, paypal, etc.
    status = Column(String, default="pending")  # pending, completed, failed, refunded
    transaction_id = Column(String)  # External payment processor ID
    payment_date = Column(DateTime, default=datetime.utcnow)
    invoice = relationship("Invoice", back_populates="payments")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, amount={self.amount}, status={self.status})>"

    @classmethod
    async def create(cls, **kwargs):
        payment = cls(id=str(uuid4()), **kwargs)
        db.add(payment)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return payment

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def all_payments(cls):
        query = select(cls)
        payments = await db.execute(query)
        return payments.scalars().all()

    @classmethod
    async def get_id(cls, id):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    plan_name = Column(String)
    amount = Column(Integer)  # Store in cents
    currency = Column(String, default="USD")
    status = Column(String, default="active")  # active, cancelled, paused
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    billing_cycle = Column(String)  # monthly, yearly
    customer = relationship("Customer", back_populates="subscriptions")
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, plan_name={self.plan_name}, status={self.status})>"

    @classmethod
    async def create(cls, **kwargs):
        subscription = cls(id=str(uuid4()), **kwargs)
        db.add(subscription)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return subscription

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def all_subscriptions(cls):
        query = select(cls)
        subscriptions = await db.execute(query)
        return subscriptions.scalars().all()

    @classmethod
    async def get_id(cls, id):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True


# Update Customer model to include relationships
Customer.invoices = relationship("Invoice", back_populates="customer")
Customer.subscriptions = relationship("Subscription", back_populates="customer")

# Update Invoice model to include relationships
Invoice.payments = relationship("Payment", back_populates="invoice")

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(Integer)
    stage = Column(String)
    customer_id = Column(String, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="opportunities")

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, full_name={self.name}, )>"

    @classmethod
    async def create(cls, **kwargs):
        user = cls(**kwargs)
        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def all_opportunities(cls):
        query = select(cls)
        users = await db.execute(query)
        user = users.scalars().all()
        return user

    @classmethod
    async def get_id(cls, id):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user

    @classmethod
    async def delete(cls, id):
        query = sqlalchemy_delete(cls).where(cls.id == id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True
