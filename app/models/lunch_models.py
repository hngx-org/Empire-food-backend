from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Lunch(Base):
    __tablename__ = "lunches"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(
        Integer, ForeignKey("organizations.id", ondelete="CASCADE")
    )
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
    redeemed = Column(Boolean, default=False)
    note = Column(Text)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    organization = relationship("Organization", back_populates="lunches")
    sender = relationship(
        "User", backref="sender_lunches", foreign_keys=[sender_id]
    )
    receiver = relationship(
        "User", backref="receiver_lunches", foreign_keys=[receiver_id]
    )
