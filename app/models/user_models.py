from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    DECIMAL,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
    )
    first_name = Column(String(255))
    last_name = Column(String(255))
    profile_pic = Column(String(255))  # Assuming a URL
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean)
    lunch_credit_balance = Column(Integer, default=0)
    refresh_token = Column(String(255))
    bank_number = Column(String(255))
    bank_code = Column(String(255))
    bank_name = Column(String(255))
    bank_region = Column(String(255))
    currency = Column(String(128))
    currency_code = Column(String(4))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    organization = relationship("Organization", back_populates="users")
    withdrawals = relationship("Withdrawal", back_populates="user")


class Withdrawal(Base):
    __tablename__ = "withdrawals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    status = Column(
        Enum("redeemed", "not_redeemed", name="withdrawal_status"),
        nullable=False,
        default="not_redeemed",
    )
    amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="withdrawals")
