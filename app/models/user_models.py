from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from uuid import uuid4 as uuid
from datetime import datetime

class Users():
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, default=uuid)
  name = Column(String(50))
  email = Column(String(50))
  phonenumber = Column(String(50))
  password_hash = Column(String(50))
  org_id = Column(Integer, ForeignKey('organization.id'))
  refresh_token = Column(String(255))
  created_at = Column(datetime.utcnow())
  updated_at = Column(datetime.utcnow())