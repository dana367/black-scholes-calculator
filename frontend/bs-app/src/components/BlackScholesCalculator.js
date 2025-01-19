import React, { useState } from 'react';
import api from '../api'; // Import the configured API instance

const BlackScholesCalculator = () => {
  const [formData, setFormData] = useState({
    stock_price: '',
    strike_price: '',
    time_to_maturity: '',
    risk_free_rate: '',
    dividend_yield: '',
    volatility: '',
  });
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setResult(null);
    setError(null);

    try {
      const requestData = {
        stock_price: parseFloat(formData.stock_price),
        strike_price: parseFloat(formData.strike_price),
        time_to_maturity: parseFloat(formData.time_to_maturity),
        risk_free_rate: parseFloat(formData.risk_free_rate) / 100,
        dividend_yield: parseFloat(formData.dividend_yield) / 100,
        volatility: parseFloat(formData.volatility) / 100,
      };

      if (Object.values(requestData).some(isNaN)) {
        throw new Error('Please enter valid numbers for all fields.');
      }

      if (Object.values(requestData).some((value) => value <= 0)) {
        throw new Error('All values must be positive numbers.');
      }

      const response = await api.post('/calculate', requestData);

      if (!response.data || response.status >= 400) {
        throw new Error(response.data?.detail || 'Server error occurred.');
      }

      setResult({
        callOptionPrice: response.data.call_option_price,
        putOptionPrice: response.data.put_option_price,
      });
    } catch (error) {
      setError(
        error.response?.data?.detail ||
        error.message ||
        'An unexpected error occurred. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <form onSubmit={handleFormSubmit}>
        <div className="row">
          <div className="col-md-6">
            <div className="mb-3">
              <label className="form-label">Stock Price (£)</label>
              <input
                type="number"
                className="form-control"
                name="stock_price"
                value={formData.stock_price}
                onChange={handleInputChange}
                step="0.01"
                min="0.01"
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Strike Price (£)</label>
              <input
                type="number"
                className="form-control"
                name="strike_price"
                value={formData.strike_price}
                onChange={handleInputChange}
                step="0.01"
                min="0.01"
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Time to Maturity (years)</label>
              <input
                type="number"
                className="form-control"
                name="time_to_maturity"
                value={formData.time_to_maturity}
                onChange={handleInputChange}
                step="0.01"
                min="0.01"
                required
              />
            </div>
          </div>

          <div className="col-md-6">
            <div className="mb-3">
              <label className="form-label">Risk-Free Rate (%)</label>
              <input
                type="number"
                className="form-control"
                name="risk_free_rate"
                value={formData.risk_free_rate}
                onChange={handleInputChange}
                step="0.01"
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Dividend Yield (%)</label>
              <input
                type="number"
                className="form-control"
                name="dividend_yield"
                value={formData.dividend_yield}
                onChange={handleInputChange}
                step="0.01"
                min="0"
                required
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Volatility (%)</label>
              <input
                type="number"
                className="form-control"
                name="volatility"
                value={formData.volatility}
                onChange={handleInputChange}
                step="0.01"
                min="0.01"
                max="100"
                required
              />
            </div>
          </div>
        </div>

        <button type="submit" className="btn btn-primary btn-lg" disabled={isLoading}>
          {isLoading ? 'Calculating...' : 'Calculate'}
        </button>
      </form>

      {error && <div className="alert alert-danger mt-4">{error}</div>}

      {result && (
        <div className="mt-4">
          <div className="card bg-light">
            <div className="card-body">
              <h5>Call Option Price: £{result.callOptionPrice?.toFixed(4)}</h5>
              <h5>Put Option Price: £{result.putOptionPrice?.toFixed(4)}</h5>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BlackScholesCalculator;
