from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, and_
from sqlalchemy.orm import relationship
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy.future import select
import enum
from uuid import uuid4

from core.database import Base, db

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

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.full_name}, "
            f")>"
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
        users = await db.execute(query)
        (user,) = users.first()
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
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.name}, "
            f")>"
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
        users = await db.execute(query)
        (user,) = users.first()
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
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="contacts")


    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.name}, "
            f")>"
        )

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
        users = await db.execute(query)
        (user,) = users.first()
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
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="leads")


    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.name}, "
            f")>"
        )

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
        users = await db.execute(query)
        (user,) = users.first()
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

class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(Integer)
    stage = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="opportunities")


    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.name}, "
            f")>"
        )

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
        users = await db.execute(query)
        (user,) = users.first()
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