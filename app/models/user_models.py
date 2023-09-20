from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from uuid import uuid4 as uuid
from datetime import datetime


class User:
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, default=uuid)
    name = Column(String(50))
    email = Column(String(50))
    phonenumber = Column(String(50))
    password_hash = Column(String(50))
    org_id = Column(Integer, ForeignKey("organization.id"))
    refresh_token = Column(String(255))
    created_at = Column(datetime.utcnow())
    updated_at = Column(datetime.utcnow())

    class withdrawals:
        __tablename__ = "withdrawals"
        id = Column(Integer, primary_key=True, default=uuid)
        user_id = Column(Integer, ForeignKey("users.id"))
        status = Column(String(50))
        amount = Column(Integer)
        created_at = Column(datetime.utcnow())
