from sqlalchemy import Column, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RedeemLunch(Base):
    __tablename__ = "lunch_table"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    redeem = Column(Boolean, default=False)