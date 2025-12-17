import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LogOut,
  Key,
  Database,
  BarChart3,
  Sun,
  Moon
} from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [theme, setTheme] = useState('light');

  // Load saved theme
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    document.documentElement.setAttribute('data-theme', savedTheme);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav
      style={{
        background: 'var(--accent-color)',
        color: 'white',
        padding: '15px 20px',
        marginBottom: '20px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}
    >
      <div
        style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        {/* Left Section */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '30px' }}>
          <Link
            to="/dashboard"
            style={{
              color: 'white',
              textDecoration: 'none',
              fontSize: '20px',
              fontWeight: 'bold'
            }}
          >
            API Management
          </Link>

          {user && (
            <div style={{ display: 'flex', gap: '20px' }}>
              <Link to="/dashboard" style={linkStyle}>
                <Database size={18} />
                APIs
              </Link>
              <Link to="/keys" style={linkStyle}>
                <Key size={18} />
                API Keys
              </Link>
              <Link to="/analytics" style={linkStyle}>
                <BarChart3 size={18} />
                Analytics
              </Link>
            </div>
          )}
        </div>

        {/* Right Section */}
        {user && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              title="Toggle Theme"
              style={{
                background: 'transparent',
                border: '2px solid white',
                color: 'white',
                padding: '8px',
                borderRadius: '50%',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              {theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}
            </button>

            <span>{user.username}</span>

            <button
              onClick={handleLogout}
              style={{
                background: 'transparent',
                border: '1px solid white',
                color: 'white',
                padding: '8px 15px',
                borderRadius: '6px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}
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

const linkStyle = {
  color: 'white',
  textDecoration: 'none',
  display: 'flex',
  alignItems: 'center',
  gap: '5px'
};

export default Navbar;
