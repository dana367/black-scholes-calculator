import React from 'react';
import BlackScholesCalculator from './components/BlackScholesCalculator'; // Import the component

const App = () => {
  return (
    <div>
      <nav className="navbar navbar-dark bg-primary">
        <div className="container-fluid">
          <a className="navbar-brand" href="/">
            Black-Scholes Calculator
          </a>
        </div>
      </nav>

      {/* Render the Black-Scholes Calculator */}
      <BlackScholesCalculator />
    </div>
  );
};

export default App;
