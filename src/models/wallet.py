import uuid

from sqlalchemy import Column, String, Float, DateTime, func, UUID, DECIMAL

from src.database import Base


class WalletRequest(Base):
    __tablename__ = 'wallet_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4, index=True)
    address = Column(String, nullable=False, index=True)
    bandwidth = Column(Float)
    energy = Column(Float)
    trx_balance = Column(DECIMAL, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())