# Black-Scholes Option Pricing Calculator

This project is a full-stack application for calculating option prices using the Black-Scholes model.

The Black-Scholes Option Pricing Calculator is a web-based tool that allows users to calculate call and put option prices using the Black-Scholes model. It provides a user-friendly interface for inputting option parameters and displays the calculated prices. The application also stores calculation history, allowing users to review past calculations.

The calculator is built using a React.js frontend and a FastAPI backend, with a SQLite database for persistent storage. It offers real-time calculation of option prices and maintains a history of all calculations performed.

## Repository Structure

```
black-scholes-calculator/
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── formula.py
│   ├── main.py
│   └── models.py
└── frontend/
    └── bs-app/
        ├── package.json
        ├── public/
        │   ├── index.html
        │   
        └── src/
            ├── api.js
            ├── App.js
            ├── components/
            │   ├── BlackScholesCalculator.js
            │   └── HistoryTable.js
            └── index.js
```

### Key Files:

- `backend/main.py`: Entry point for the FastAPI backend application.
- `backend/formula.py`: Contains the Black-Scholes calculation logic.
- `frontend/bs-app/src/components/BlackScholesCalculator.js`: Main React component for the calculator interface.
- `frontend/bs-app/package.json`: Defines the frontend project dependencies and scripts.

### Integration Points:

- The frontend communicates with the backend via RESTful API endpoints defined in `backend/main.py`.
- The backend connects to a SQLite database using SQLAlchemy, configured in `backend/database.py`.

## Usage Instructions

### Installation

Prerequisites:
- Python 3.8+
- Node.js 14+
- npm 6+

Backend Setup:
1. Navigate to the `backend` directory:
   ```
   cd black-scholes-calculator/backend
   ```
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
4. Install the required packages:
   ```
   pip install fastapi uvicorn sqlalchemy pydantic scipy
   ```

Frontend Setup:
1. Navigate to the frontend directory:
   ```
   cd black-scholes-calculator/frontend/bs-app
   ```
2. Install the required npm packages:
   ```
   npm install
   ```

### Getting Started

1. Start the backend server:
   ```
   cd black-scholes-calculator/backend
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

2. In a new terminal, start the frontend development server:
   ```
   cd black-scholes-calculator/frontend/bs-app
   npm start
   ```
   The application will be available at `http://localhost:3000`.

3. Open a web browser and navigate to `http://localhost:3000` to use the Black-Scholes Calculator.

### Configuration

- Backend: The database URL can be configured in `backend/database.py`.
- Frontend: The API base URL can be adjusted in `frontend/bs-app/src/api.js` if needed.

### Common Use Cases

1. Calculating Option Prices:
   - Enter the required parameters (stock price, strike price, time to maturity, risk-free rate, dividend yield, and volatility) in the form.
   - Click the "Calculate" button to get the call and put option prices.

2. Viewing Calculation History:
   - Click the "View History" button to see a table of all past calculations.

### Integration Patterns

The frontend uses Axios to make HTTP requests to the backend API. The main integration points are:

- POST request to `/calculate` for performing Black-Scholes calculations.
- GET request to `/calculations` for retrieving the calculation history.

### Testing & Quality

To run the frontend tests:
```
cd black-scholes-calculator/frontend/bs-app
npm test
```

### Troubleshooting

Common Issue: API Connection Error
- Problem: The frontend fails to connect to the backend API.
- Error Message: "Network Error" or "Failed to fetch"
- Diagnostic Steps:
  1. Ensure the backend server is running on `http://localhost:8000`.
  2. Check if CORS is properly configured in `backend/main.py`.
  3. Verify the API base URL in `frontend/bs-app/src/api.js`.
- Solution: If the backend is running on a different port or host, update the `baseURL` in `api.js` accordingly.

Debugging:
- Backend: Use `print()` statements or configure logging in `main.py` for debugging.
- Frontend: Use browser developer tools to inspect network requests and console logs.

Performance Optimization:
- Monitor API response times for `/calculate` endpoint.
- Use browser performance tools to profile the frontend application.
- Consider implementing caching for frequently used calculations.

## Data Flow

The Black-Scholes Calculator application follows a client-server architecture with a clear separation between the frontend and backend components.

1. User Input: The user enters option parameters in the React frontend.
2. API Request: The frontend sends a POST request to the `/calculate` endpoint of the FastAPI backend.
3. Calculation: The backend processes the request, performs the Black-Scholes calculation using the `formula.py` module.
4. Database Storage: The calculation result is stored in the SQLite database using SQLAlchemy.
5. API Response: The backend sends the calculated option prices back to the frontend.
6. Display: The frontend displays the results to the user.
7. History Retrieval: When requested, the frontend fetches calculation history from the `/calculations` endpoint.

```
[User] -> [React Frontend] -> [FastAPI Backend] -> [SQLite Database]
   ^            |                    |                    |
   |            |                    |                    |
   +------------+--------------------+--------------------+
```

Note: The backend uses SQLAlchemy as an ORM to interact with the SQLite database, providing a layer of abstraction for database operations.