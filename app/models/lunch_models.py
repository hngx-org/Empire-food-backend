from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from uuid import uuid4 as uuid
from datetime import datetime



class Lunches():
  id = Column(Integer, primary_key=True, default=uuid)
  senderId = Column(String(50)) 
  receiverId = Column(String(50))
  quantity = Column(Integer)
  redeemed = Column(Boolean)
  created_at = Column(DateTime, default=datetime.utcnow())
  note = Column(Text)