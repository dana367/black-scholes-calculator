from database import Base
from sqlalchemy import Column, DateTime, Float, Integer, func


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    stock_price = Column(Float, nullable=False)
    strike_price = Column(Float, nullable=False)
    time_to_maturity = Column(Float, nullable=False)
    risk_free_rate = Column(Float, nullable=False)
    dividend_yield = Column(Float, nullable=False)
    volatility = Column(Float, nullable=False)
    call_option_price = Column(Float, nullable=False)
    put_option_price = Column(Float, nullable=False)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
