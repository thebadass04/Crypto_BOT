from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Side(str, Enum):
    BUY = "Buy"
    SELL = "Sell"


class OrderType(str, Enum):
    MARKET = "Market"
    LIMIT = "Limit"


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class OrderRequest(BaseModel):
    symbol: str = Field(..., description="Trading symbol (e.g., BTCUSDT)")
    side: Side = Field(..., description="Order side: Buy or Sell")
    order_type: OrderType = Field(..., description="Order type: Market or Limit")
    qty: float = Field(..., description="Order quantity", gt=0)
    price: Optional[float] = Field(None, description="Price for limit orders", gt=0)
    

class OrderResponse(BaseModel):
    order_id: str
    symbol: str
    side: str
    order_type: str
    qty: float
    price: Optional[float]
    status: str
    created_time: str


class Position(BaseModel):
    symbol: str
    side: str
    size: float
    entry_price: float
    mark_price: float
    unrealised_pnl: float
    leverage: float


class Balance(BaseModel):
    coin: str
    wallet_balance: float
    available_balance: float
    equity: float


class PriceData(BaseModel):
    symbol: str
    price: float
    timestamp: int


class Kline(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class SignalResponse(BaseModel):
    symbol: str
    signal: Signal
    sma_fast: float
    sma_slow: float
    current_price: float
    timestamp: str


class AccountInfo(BaseModel):
    uid: str
    account_type: str
    status: str
    balances: List[Balance]
