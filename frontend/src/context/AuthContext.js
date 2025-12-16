import React, { createContext, useState, useContext, useEffect } from 'react';
import * as api from '../utils/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const token = localStorage.getItem('access_token');

    if (storedUser && token) {
      setUser(JSON.parse(storedUser));
      fetchUserSettings();
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const response = await api.authAPI.login({ email, password });
    const { user, access_token, refresh_token } = response.data;

    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user', JSON.stringify(user));

    setUser(user);
    await fetchUserSettings();
    return response.data;
  };

  const register = async (username, email, password) => {
    const response = await api.authAPI.register({ username, email, password });
    const { user, access_token, refresh_token } = response.data;

    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user', JSON.stringify(user));

    setUser(user);
    return response.data;
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    setUser(null);
    setTheme('light');
    document.documentElement.removeAttribute('data-theme');
  };

  const applyTheme = (newTheme) => {
    setTheme(newTheme);
    if (newTheme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  };

  const fetchUserSettings = async () => {
    try {
      const response = await api.userAPI.getProfile();
      const userSettings = response.data.settings;
      if (userSettings && userSettings.theme) {
        applyTheme(userSettings.theme);
      }
    } catch (error) {
      console.error('Failed to fetch user settings:', error);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading, theme, applyTheme, fetchUserSettings }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
