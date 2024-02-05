import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  // Check if the user is authenticated by looking for a token in localStorage
  const isAuthenticated = localStorage.getItem('token') !== null;

  const handleLogout = () => {
    // Remove the token from localStorage to log the user out
    localStorage.removeItem('token');
    // Redirect to the sign-in page. This could be enhanced with React Router's `useNavigate` for SPA behavior
    window.location.href = '/signin';
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container">
        <Link className="navbar-brand" to="/">
          Critiq Hub
        </Link>
        <div className="collapse navbar-collapse" id="navbarNav">
          <div className="search-container">
            <input
              type="text"
              placeholder="Type Your Search"
              className="form-control search-input"
            />
            <button className="btn btn-outline-secondary search-button">
              Search
            </button>
          </div>

          <ul className="navbar-nav ml-auto">
            <li className="nav-item active">
              <Link className="nav-link" to="/">
                Home
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/categories">
                All Categories
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/review">
                Write A Review
              </Link>
            </li>
            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                href="#"
                id="moreDropdown"
                role="button"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
              >
                More
              </a>
              <div className="dropdown-menu" aria-labelledby="moreDropdown">
                <Link className="dropdown-item" to="/movies">
                  Movies
                </Link>
                <Link className="dropdown-item" to="/restaurants">
                  Restaurants
                </Link>
                <Link className="dropdown-item" to="/books">
                  Books
                </Link>
              </div>
            </li>
          </ul>

          <div className="auth-buttons">
            {!isAuthenticated ? (
              <>
                <Link to="/signin" className="btn btn-outline-primary auth-button">
                  Sign In
                </Link>
                <Link to="/signup" className="btn btn-primary auth-button">
                  Sign Up
                </Link>
                <Link to="/reset-password" className="btn btn-primary auth-button">
                  Reset Password
                </Link>
              </>
            ) : (
              <button onClick={handleLogout} className="btn btn-danger auth-button">
                Logout
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
