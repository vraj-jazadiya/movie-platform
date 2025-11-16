import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../App';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div className="navbar-content">
          <Link to="/" className="navbar-brand">
            <span className="brand-icon">🎬</span>
            <span className="brand-text">MoviePlatform</span>
          </Link>

          <div className="navbar-menu">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/news" className="nav-link">News</Link>
            {user && <Link to="/profile" className="nav-link">Profile</Link>}
            {user && <Link to="/chat" className="nav-link">Chat</Link>}
            <Link to="/contact" className="nav-link">Contact</Link>
            {user?.role === 'admin' && (
              <Link to="/admin" className="nav-link admin-link">Admin</Link>
            )}
          </div>

          <div className="navbar-actions">
            {user ? (
              <>
                <span className="user-greeting">Hi, {user.name || user.username}!</span>
                <button onClick={handleLogout} className="btn btn-secondary">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="btn btn-secondary">Login</Link>
                <Link to="/register" className="btn btn-primary">Sign Up</Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
