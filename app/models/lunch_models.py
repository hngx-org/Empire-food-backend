from sqlalchemy import Column, Integer, String, Boolean,Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base



class Lunch(Base):
  __tablename__ = 'lunches'
  id = Column(Integer, primary_key=True, index=True)
  org_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))
  sender_id = Column(Integer)
  receiver_id = Column(Integer)
  quantity = Column(Integer, nullable=False)
  redeemed = Column(Boolean, default=False)
  created_at = Column(DateTime, server_default=func.now())
  is_deleted = Column(Boolean, default=False)
  note = Column(Text)
  organization = relationship("Organization", back_populates="lunches")
 

