import React, { useState, useEffect } from 'react';
import { userAPI } from '../utils/api';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';
import { Save, Moon, Sun, Bell, Zap } from 'lucide-react';

const Settings = () => {
  const { theme, applyTheme } = useAuth();
  const [settings, setSettings] = useState({
    theme: 'light',
    email_notifications: true,
    default_rate_limit: 1000
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await userAPI.getProfile();
      if (response.data.settings) {
        setSettings(response.data.settings);
      }
    } catch (error) {
      console.error(error);
      if (error.response?.status === 404) {
        toast.error('User not found. Please log in again.');
        // Clear local storage and redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return;
      }
      toast.error('Failed to fetch settings');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;
    setSettings(prev => ({
      ...prev,
      [name]: newValue
    }));

    // Apply theme immediately when theme changes
    if (name === 'theme') {
      applyTheme(newValue);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await userAPI.updateSettings(settings);
      toast.success('Settings updated successfully');
    } catch (error) {
      console.error(error);
      toast.error(error.response?.data?.error || 'Failed to update settings');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '40px' }}>Loading...</div>;
  }

  return (
    <div className="container">
      <h1>User Settings</h1>
      <div className="card" style={{ maxWidth: '600px', margin: '0 auto', padding: '30px' }}>
        <form onSubmit={handleSubmit}>
          
          {/* Theme Setting */}
          <div style={{ marginBottom: '25px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px', fontWeight: '500' }}>
              {settings.theme === 'light' ? <Sun size={20} /> : <Moon size={20} />}
              Theme
            </label>
            <div style={{ display: 'flex', gap: '15px' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="theme"
                  value="light"
                  checked={settings.theme === 'light'}
                  onChange={handleChange}
                />
                Light
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                <input
                  type="radio"
                  name="theme"
                  value="dark"
                  checked={settings.theme === 'dark'}
                  onChange={handleChange}
                />
                Dark
              </label>
            </div>
          </div>

          {/* Email Notifications Setting */}
          <div style={{ marginBottom: '25px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px', fontWeight: '500' }}>
              <Bell size={20} />
              Notifications
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
              <input
                type="checkbox"
                name="email_notifications"
                checked={settings.email_notifications}
                onChange={handleChange}
                style={{ width: '18px', height: '18px' }}
              />
              Receive email notifications
            </label>
          </div>

          {/* Default Rate Limit Setting */}
          <div style={{ marginBottom: '30px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px', fontWeight: '500' }}>
              <Zap size={20} />
              Default Rate Limit (requests/hour)
            </label>
            <input
              type="number"
              name="default_rate_limit"
              value={settings.default_rate_limit}
              onChange={handleChange}
              min="1"
              style={{
                width: '100%',
                padding: '10px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={saving}
            style={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '10px' }}
          >
            <Save size={18} />
            {saving ? 'Saving...' : 'Save Settings'}
          </button>

        </form>
      </div>
    </div>
  );
};

export default Settings;
