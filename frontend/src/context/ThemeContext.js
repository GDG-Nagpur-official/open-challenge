import { createContext, useState, useContext, useEffect } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    console.log('Loading theme from localStorage:', saved);
    if (saved !== null) {
      return JSON.parse(saved);
    }
    // Check system preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    console.log('System prefers dark:', prefersDark);
    return prefersDark;
  });

  useEffect(() => {
    console.log('Saving theme to localStorage:', isDarkMode);
    localStorage.setItem('darkMode', JSON.stringify(isDarkMode));
    
    console.log('Applying theme to document:', isDarkMode ? 'dark' : 'light');
    const html = document.documentElement;
    if (isDarkMode) {
      html.setAttribute('data-theme', 'dark');
      html.classList.add('dark');
      document.body.classList.add('dark');
      // Force background color
      document.body.style.backgroundColor = '#1a1a1a';
      document.body.style.color = '#e0e0e0';
    } else {
      html.setAttribute('data-theme', 'light');
      html.classList.remove('dark');
      document.body.classList.remove('dark');
      document.body.style.backgroundColor = '';
      document.body.style.color = '';
    }
  }, [isDarkMode]);

  const toggleTheme = () => {
    console.log('Toggling theme from', isDarkMode, 'to', !isDarkMode);
    setIsDarkMode(!isDarkMode);
  };

  return (
    <ThemeContext.Provider value={{ isDarkMode, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    console.error('useTheme must be used within ThemeProvider');
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}