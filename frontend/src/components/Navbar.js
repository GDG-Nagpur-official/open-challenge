import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { LogOut, Key, Database, BarChart3, Moon, Sun } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-left">
          <Link to="/dashboard" className="navbar-brand">
            API Management
          </Link>
          {user && (
            <div className="navbar-links">
              <Link to="/dashboard" className="navbar-link">
                <Database size={18} />
                APIs
              </Link>
              <Link to="/keys" className="navbar-link">
                <Key size={18} />
                API Keys
              </Link>
              <Link to="/analytics" className="navbar-link">
                <BarChart3 size={18} />
                Analytics
              </Link>
            </div>
          )}
        </div>
        {user && (
          <div className="navbar-right">
            <span>{user.username}</span>
            <button
              onClick={toggleTheme}
              className="theme-toggle"
              aria-label="Toggle theme"
            >
              {theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}
            </button>
            <button
              onClick={handleLogout}
              className="logout-btn"
            >
              <LogOut size={18} />
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
