import React from 'react';
import { useTheme } from './ThemeContext';
import { Sun, Moon } from 'lucide-react';
import './ThemeToggle.css';

const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      className="theme-toggle"
      onClick={toggleTheme}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      <div className={`theme-toggle-slider ${theme === 'dark' ? 'dark' : 'light'}`}>
        <div className="theme-toggle-icon">
          {theme === 'light' ? (
            <Sun size={16} />
          ) : (
            <Moon size={16} />
          )}
        </div>
      </div>
    </button>
  );
};

export default ThemeToggle;

