import React, { useEffect, useState } from 'react';
import api from '../api';

const HistoryTable = ({ onBack }) => {
  const [calculations, setCalculations] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCalculations = async () => {
      try {
        const response = await api.get('/black-scholes/calculations');
        setCalculations(response.data);
      } catch (err) {
        setError('Failed to fetch calculations. Please try again later.');
      }
    };

    fetchCalculations();
  }, []);

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Calculation History</h2>
        <button className="btn btn-primary" onClick={onBack}>
          Back to Calculator
        </button>
      </div>
      {calculations.length === 0 ? (
        <p>No calculations found.</p>
      ) : (
        <table className="table table-striped table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Stock Price (£)</th>
              <th>Strike Price (£)</th>
              <th>Time to Maturity (Years)</th>
              <th>Risk-Free Rate (%)</th>
              <th>Dividend Yield (%)</th>
              <th>Volatility (%)</th>
              <th>Call Option Price (£)</th>
              <th>Put Option Price (£)</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {calculations.map((calc) => (
              <tr key={calc.id}>
                <td>{calc.id}</td>
                <td>£{calc.stock_price.toFixed(2)}</td>
                <td>£{calc.strike_price.toFixed(2)}</td>
                <td>{calc.time_to_maturity.toFixed(2)}</td>
                <td>{(calc.risk_free_rate * 100).toFixed(2)}%</td>
                <td>{(calc.dividend_yield * 100).toFixed(2)}%</td>
                <td>{(calc.volatility * 100).toFixed(2)}%</td>
                <td>£{calc.call_option_price.toFixed(4)}</td>
                <td>£{calc.put_option_price.toFixed(4)}</td>
                <td>{calc.timestamp ? new Date(calc.timestamp).toLocaleString() : 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default HistoryTable;
