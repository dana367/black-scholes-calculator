# backend/test/test_main.py
import os
import sys
from pathlib import Path

# Add the parent directory to PYTHONPATH
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from datetime import datetime
from typing import List

import pytest
from database import Base
from fastapi.testclient import TestClient
from main import app, get_db
from models import Calculation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestMain:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Reset database before each test"""
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def test_calculate_valid_input(self):
        """Test calculation with valid input data."""
        input_data = {
            "stock_price": 100.0,
            "strike_price": 100.0,
            "time_to_maturity": 1.0,
            "risk_free_rate": 0.05,
            "dividend_yield": 0.02,
            "volatility": 0.2,
        }

        response = client.post("/calculate", json=input_data)
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)
        assert "id" in result
        assert "call_option_price" in result
        assert "put_option_price" in result
        assert "timestamp" in result
        assert result["call_option_price"] > 0
        assert result["put_option_price"] > 0

    def test_calculate_invalid_input(self):
        """Test calculation with invalid input."""
        invalid_input = {
            "stock_price": -100.0,  # Invalid negative value
            "strike_price": 100.0,
            "time_to_maturity": 1.0,
            "risk_free_rate": 0.05,
            "dividend_yield": 0.02,
            "volatility": 0.2,
        }

        response = client.post("/calculate", json=invalid_input)
        assert response.status_code == 422

    def test_get_calculations(self):
        """Test getting all calculations."""
        # First, add some test data
        input_data = {
            "stock_price": 100.0,
            "strike_price": 100.0,
            "time_to_maturity": 1.0,
            "risk_free_rate": 0.05,
            "dividend_yield": 0.02,
            "volatility": 0.2,
        }
        # Add test calculation
        calc_response = client.post("/calculate", json=input_data)
        assert calc_response.status_code == 200

        # Test get calculations endpoint
        response = client.get("/calculations")
        assert response.status_code == 200
        calculations = response.json()
        assert isinstance(calculations, list)
        assert len(calculations) > 0

        # Verify calculation data
        first_calc = calculations[0]
        assert "id" in first_calc
        assert "call_option_price" in first_calc
        assert "put_option_price" in first_calc
        assert "timestamp" in first_calc
        assert "stock_price" in first_calc
        assert "strike_price" in first_calc
        assert "time_to_maturity" in first_calc
        assert "risk_free_rate" in first_calc
        assert "dividend_yield" in first_calc
        assert "volatility" in first_calc

    def test_multiple_calculations(self):
        """Test multiple calculations and retrieval."""
        # Add multiple calculations
        input_data_list = [
            {
                "stock_price": 100.0,
                "strike_price": 100.0,
                "time_to_maturity": 1.0,
                "risk_free_rate": 0.05,
                "dividend_yield": 0.02,
                "volatility": 0.2,
            },
            {
                "stock_price": 150.0,
                "strike_price": 140.0,
                "time_to_maturity": 2.0,
                "risk_free_rate": 0.06,
                "dividend_yield": 0.03,
                "volatility": 0.25,
            },
        ]

        # Add test calculations
        for input_data in input_data_list:
            response = client.post("/calculate", json=input_data)
            assert response.status_code == 200

        # Verify all calculations are retrieved
        response = client.get("/calculations")
        assert response.status_code == 200
        calculations = response.json()
        assert len(calculations) == len(input_data_list)

    def test_error_handling(self):
        """Test error handling for invalid requests."""
        # Test missing required field
        invalid_input = {"stock_price": 100.0}  # Missing other required fields
        response = client.post("/calculate", json=invalid_input)
        assert response.status_code == 422

        # Test invalid type
        invalid_input = {
            "stock_price": "not a number",
            "strike_price": 100.0,
            "time_to_maturity": 1.0,
            "risk_free_rate": 0.05,
            "dividend_yield": 0.02,
            "volatility": 0.2,
        }
        response = client.post("/calculate", json=invalid_input)
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main(["-v"])
