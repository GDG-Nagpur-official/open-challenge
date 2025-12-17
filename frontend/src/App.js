import React, { useState } from 'react';

import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import APIKeys from './components/APIKeys';
import Analytics from './components/Analytics';
import Navbar from './components/Navbar';
import PrivateRoute from './components/PrivateRoute';

function App() {
    const [darkMode, setDarkMode] = useState(false);
  return (
    <AuthProvider>
      <Router>
       <div
  className="App"
  style={{
    backgroundColor: darkMode ? '#1e1e1e' : '#ffffff',
    color: darkMode ? '#ffffff' : '#000000',
    minHeight: '100vh',
  }}
>

          <Navbar />
       <button
  onClick={() => setDarkMode(!darkMode)}
  style={{
    padding: '5px 10px',
    margin: '10px',
    cursor: 'pointer',
  }}
>
  {darkMode ? '🌙 Dark Mode' : '☀️ Light Mode'}
</button>

          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/dashboard"
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              }
            />
            <Route
              path="/keys"
              element={
                <PrivateRoute>
                  <APIKeys />
                </PrivateRoute>
              }
            />
            <Route
              path="/analytics"
              element={
                <PrivateRoute>
                  <Analytics />
                </PrivateRoute>
              }
            />
          </Routes>
          <ToastContainer
            position="top-right"
            autoClose={3000}
            hideProgressBar={false}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
          />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
