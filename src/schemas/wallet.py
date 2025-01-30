from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, UUID4


class WalletRequestSchema(BaseModel):
    address: str


class WalletResponse(BaseModel):
    id: UUID4
    address: str
    bandwidth: float
    trx_balance: Decimal
    energy: float
    timestamp: datetime

    class Config:
        from_attributes = True


