from datetime import datetime

from pydantic import BaseModel, Field


class BlackScholesInput(BaseModel):
    """Input schema for Black-Scholes calculation."""

    stock_price: float = Field(..., gt=0, description="Current stock price")
    strike_price: float = Field(..., gt=0, description="Strike price")
    time_to_maturity: float = Field(..., gt=0, description="Time to maturity in years")
    risk_free_rate: float = Field(..., ge=0, description="Risk-free interest rate")
    dividend_yield: float = Field(..., ge=0, description="Dividend yield")
    volatility: float = Field(..., gt=0, le=1, description="Volatility")


class BlackScholesOutput(BaseModel):
    """Output schema for Black-Scholes calculation."""

    id: int
    call_option_price: float
    put_option_price: float
    timestamp: datetime | None = None

    class Config:
        from_attributes = True


class BlackScholesRecord(BaseModel):
    """Schema for a Black-Scholes history records"""

    id: int
    stock_price: float
    strike_price: float
    time_to_maturity: float
    risk_free_rate: float
    dividend_yield: float
    volatility: float
    call_option_price: float
    put_option_price: float
    timestamp: datetime | None = None

    class Config:
        from_attributes = True
