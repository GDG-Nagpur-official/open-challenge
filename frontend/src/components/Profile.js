import React, { useState, useEffect } from 'react';
import { userAPI } from '../utils/api';
import { toast } from 'react-toastify';
import { User, Mail, Calendar, Clock } from 'lucide-react';

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await userAPI.getProfile();
      setProfile(response.data);
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
      toast.error('Failed to fetch profile');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '40px' }}>Loading...</div>;
  }

  if (!profile) {
    return <div style={{ textAlign: 'center', padding: '40px' }}>Profile not found</div>;
  }

  return (
    <div className="container">
      <h1>User Profile</h1>
      <div className="card" style={{ maxWidth: '600px', margin: '0 auto', padding: '30px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', padding: '10px', borderBottom: '1px solid #eee' }}>
            <User size={24} color="#666" />
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#888', marginBottom: '4px' }}>Username</label>
              <span style={{ fontSize: '16px', fontWeight: '500' }}>{profile.username}</span>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', padding: '10px', borderBottom: '1px solid #eee' }}>
            <Mail size={24} color="#666" />
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#888', marginBottom: '4px' }}>Email</label>
              <span style={{ fontSize: '16px', fontWeight: '500' }}>{profile.email}</span>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', padding: '10px', borderBottom: '1px solid #eee' }}>
            <Calendar size={24} color="#666" />
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#888', marginBottom: '4px' }}>Account Created</label>
              <span style={{ fontSize: '16px', fontWeight: '500' }}>
                {new Date(profile.created_at).toLocaleDateString()} {new Date(profile.created_at).toLocaleTimeString()}
              </span>
            </div>
          </div>

          {profile.updated_at && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', padding: '10px' }}>
              <Clock size={24} color="#666" />
              <div>
                <label style={{ display: 'block', fontSize: '12px', color: '#888', marginBottom: '4px' }}>Last Updated</label>
                <span style={{ fontSize: '16px', fontWeight: '500' }}>
                  {new Date(profile.updated_at).toLocaleDateString()} {new Date(profile.updated_at).toLocaleTimeString()}
                </span>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default Profile;
