import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-dark bg-primary">
      <div className="container-fluid">
        <a className="navbar-brand" href={user ? "/calculator" : "/login"}>
          Black-Scholes Calculator
        </a>
        {user && (
          <div className="d-flex">
            <span className="navbar-text me-3">
              Welcome, {user.username}
            </span>
            <button 
              className="btn btn-outline-light"
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
