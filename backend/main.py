from datetime import datetime
from typing import Annotated, List

import models
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from formula import calculate_black_scholes
from models import Calculation
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)


@app.post("/calculate", response_model=BlackScholesOutput)
async def calculate(input_data: BlackScholesInput, db: db_dependency):
    try:
        results = calculate_black_scholes(
            S=input_data.stock_price,
            X=input_data.strike_price,
            T=input_data.time_to_maturity,
            r=input_data.risk_free_rate,
            q=input_data.dividend_yield,
            v=input_data.volatility,
        )

        calculation = Calculation(
            stock_price=input_data.stock_price,
            strike_price=input_data.strike_price,
            time_to_maturity=input_data.time_to_maturity,
            risk_free_rate=input_data.risk_free_rate,
            dividend_yield=input_data.dividend_yield,
            volatility=input_data.volatility,
            call_option_price=results["call_option_price"],
            put_option_price=results["put_option_price"],
            # timestamp will be automatically set by the database default
        )

        db.add(calculation)
        db.commit()
        db.refresh(calculation)

        return BlackScholesOutput(
            id=calculation.id,
            call_option_price=calculation.call_option_price,
            put_option_price=calculation.put_option_price,
            timestamp=calculation.timestamp,
        )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/calculations", response_model=List[BlackScholesRecord])
async def get_calculations(db: db_dependency):
    """
    Retrieve all saved Black-Scholes calculations.
    """
    try:
        calculations = db.query(Calculation).all()
        return calculations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
