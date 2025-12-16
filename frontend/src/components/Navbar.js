import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { LogOut, Key, Database, BarChart3, Sun, Moon } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isDark = theme === 'dark';

  return (
    <nav style={{
      background: '#007bff',
      color: 'white',
      padding: '15px 20px',
      marginBottom: '20px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '30px' }}>
          <Link to="/dashboard" style={{ color: 'white', textDecoration: 'none', fontSize: '20px', fontWeight: 'bold' }}>
            API Management
          </Link>
          {user && (
            <div style={{ display: 'flex', gap: '20px' }}>
              <Link to="/dashboard" style={{ color: 'white', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '5px' }}>
                <Database size={18} />
                APIs
              </Link>
              <Link to="/keys" style={{ color: 'white', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '5px' }}>
                <Key size={18} />
                API Keys
              </Link>
              <Link to="/analytics" style={{ color: 'white', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '5px' }}>
                <BarChart3 size={18} />
                Analytics
              </Link>
            </div>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button
            type="button"
            onClick={toggleTheme}
            role="switch"
            aria-checked={isDark}
            aria-label="Toggle dark mode"
            title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
            style={{
              background: 'rgba(255,255,255,0.15)',
              border: '1px solid rgba(255,255,255,0.5)',
              color: 'white',
              padding: '8px 10px',
              borderRadius: '999px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'background 0.2s ease'
            }}
          >
            {isDark ? <Moon size={18} /> : <Sun size={18} />}
            <span style={{ fontSize: '13px', fontWeight: 600 }}>{isDark ? 'Dark' : 'Light'}</span>
          </button>

          {user && (
            <>
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
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
