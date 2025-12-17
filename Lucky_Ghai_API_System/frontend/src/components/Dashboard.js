import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [stats, setStats] = useState({ total_requests: 0, errors: 0, active_apis: 0 });
  const [logs, setLogs] = useState([]);
  const [developer, setDeveloper] = useState("Loading...");

  useEffect(() => {
    // 1. Fetch Developer Identity (Proof of Work)
    fetch('http://localhost:5000/api/developer')
      .then(res => res.json())
      .then(data => setDeveloper(data.developer))
      .catch(err => console.log("Backend offline"));

    // 2. Simulate Dashboard Data (Since DB is new)
    setStats({ total_requests: 124, errors: 2, active_apis: 3 });
    setLogs([
        { time: "10:00:01", method: "GET", endpoint: "/api/users", status: 200 },
        { time: "10:00:05", method: "POST", endpoint: "/api/auth", status: 201 },
        { time: "10:01:20", method: "GET", endpoint: "/api/dashboard", status: 500 },
        { time: "10:02:15", method: "GET", endpoint: "/api/keys", status: 200 },
    ]);
  }, []);

  return (
    <div className="dashboard-content" style={{ padding: '20px' }}>
      {/* Header Section */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <div>
            <h1 style={{ margin: 0, color: '#2d3748' }}>API Monitor</h1>
            <p style={{ margin: 0, color: '#718096' }}>Developer: <strong>{developer}</strong></p>
        </div>
        <div style={{ background: '#e2e8f0', padding: '5px 10px', borderRadius: '5px' }}>
            Status: 🟢 Online
        </div>
      </div>

      {/* Stats Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px', marginBottom: '30px' }}>
        <div className="card" style={cardStyle}>
          <h3 style={cardTitleStyle}>Total Requests</h3>
          <p style={cardNumberStyle}>{stats.total_requests}</p>
        </div>
        <div className="card" style={cardStyle}>
          <h3 style={cardTitleStyle}>Active APIs</h3>
          <p style={cardNumberStyle}>{stats.active_apis}</p>
        </div>
        <div className="card" style={cardStyle}>
          <h3 style={cardTitleStyle}>Error Rate</h3>
          <p style={{ ...cardNumberStyle, color: '#e53e3e' }}>{stats.errors}%</p>
        </div>
      </div>

      {/* Logs Table (Solves Issue #16) */}
      <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
        <h2 style={{ marginTop: 0, color: '#4a5568' }}>Live Traffic Logs</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '15px' }}>
          <thead>
            <tr style={{ textAlign: 'left', borderBottom: '2px solid #edf2f7' }}>
              <th style={{ padding: '10px' }}>Time</th>
              <th style={{ padding: '10px' }}>Method</th>
              <th style={{ padding: '10px' }}>Endpoint</th>
              <th style={{ padding: '10px' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log, index) => (
              <tr key={index} style={{ borderBottom: '1px solid #edf2f7' }}>
                <td style={{ padding: '10px', color: '#718096' }}>{log.time}</td>
                <td style={{ padding: '10px' }}>
                    <span style={{ 
                        background: log.method === 'GET' ? '#ebf8ff' : '#f0fff4', 
                        color: log.method === 'GET' ? '#3182ce' : '#38a169',
                        padding: '4px 8px', borderRadius: '4px', fontWeight: 'bold', fontSize: '0.8rem'
                    }}>
                        {log.method}
                    </span>
                </td>
                <td style={{ padding: '10px', fontWeight: '500' }}>{log.endpoint}</td>
                <td style={{ padding: '10px' }}>
                    <span style={{ color: log.status === 200 || log.status === 201 ? '#38a169' : '#e53e3e', fontWeight: 'bold' }}>
                        {log.status}
                    </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Internal Styles to keep it simple
const cardStyle = {
    background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
};
const cardTitleStyle = { margin: '0 0 10px 0', color: '#718096', fontSize: '0.9rem' };
const cardNumberStyle = { fontSize: '2rem', fontWeight: 'bold', margin: 0, color: '#2d3748' };

export default Dashboard;