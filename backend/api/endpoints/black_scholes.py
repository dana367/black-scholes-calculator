from typing import Annotated, List

from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from formula import calculate_black_scholes
from models import Calculation
from schemas.black_scholes_schema import (
    BlackScholesInput,
    BlackScholesOutput,
    BlackScholesRecord,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/black-scholes", tags=["black-scholes"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post(
    "/calculate", response_model=BlackScholesOutput, summary="Calculate options price"
)
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


@router.get(
    "/calculations",
    response_model=List[BlackScholesRecord],
    summary="Get all saved calculations",
)
async def get_calculations(db: db_dependency):
    """
    Retrieve all saved Black-Scholes calculations.
    """
    try:
        calculations = db.query(Calculation).all()
        return calculations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
