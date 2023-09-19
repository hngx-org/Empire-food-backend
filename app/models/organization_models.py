from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from uuid import uuid4 as uuid
from datetime import datetime



class orgnization_lunch_wallet():
  __tablename__ = 'organization_lunch_wallet'
  id = Column(Integer, primary_key=True, default=uuid)
  org_id = Column(Integer)
  balance = Column(Integer)


class orgnization():
  __tablename__ = 'organization'
  id = Column(Integer, primary_key=True, default=uuid)
  name = Column(String(50))
  launch_price = Column(Integer)
  currency = Column(String(50))


  class organization_invites():
    __tablename__ = 'organization_invites'
    id = Column(Integer, primary_key=True, default=uuid)
    email = Column(String(50))
    TTL = Column(Integer)