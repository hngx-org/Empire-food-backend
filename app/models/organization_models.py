from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4 as uuid
from app.db.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    lunch_price = Column(DECIMAL(10, 2), nullable=False)
    currency_code = Column(String(4), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    users = relationship("User", back_populates="organization")
    wallets = relationship("OrganizationLaunchWallet", back_populates="organization")
    invites = relationship("OrganizationInvite", back_populates="organization")
    lunches = relationship("Lunch", back_populates="organization")


class OrganizationLaunchWallet(Base):
    __tablename__ = "organization_lunch_wallets"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(DECIMAL(10, 2), nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    organization = relationship("Organization", back_populates="wallets")


class OrganizationInvite(Base):
    __tablename__ = "organization_invites"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False)
    ttl = Column(DateTime, nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    organization = relationship("Organization", back_populates="invites")
