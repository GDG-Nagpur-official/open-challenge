import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [stats, setStats] = useState({ total_requests: 0, errors: 0, active_apis: 0 });
  const [logs, setLogs] = useState([]);
  const [developer, setDeveloper] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/developer')
      .then(res => res.json())
      .then(data => setDeveloper(data))
      .catch(err => console.log("Backend not connected yet"));
    setStats({ total_requests: 124, errors: 2, active_apis: 3 });
    setLogs([
        { time: "10:00:01", method: "GET", url: "/api/users", status: 200 },
        { time: "10:00:05", method: "POST", url: "/api/auth", status: 200 },
        { time: "10:01:20", method: "GET", url: "/api/dashboard", status: 500 },
    ]);
  }, []);

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>🚀 API Manager</h2>
        <nav>
          <a href="#" className="active">Dashboard</a>
          <a href="#">APIs</a>
          <a href="#">Analytics</a>
          <a href="#">Settings</a>
        </nav>
        <div className="dev-profile">
            <p>Developer:</p>
            <strong>{developer ? developer.developer : "Loading..."}</strong>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header>
          <h1>Overview (Buildathon 2025)</h1>
          <button className="create-btn">+ New API</button>
        </header>

        {/* Stats Row */}
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Requests</h3>
            <p className="number">{stats.total_requests}</p>
          </div>
          <div className="stat-card">
            <h3>Active APIs</h3>
            <p className="number">{stats.active_apis}</p>
          </div>
          <div className="stat-card error">
            <h3>Error Rate</h3>
            <p className="number">{stats.errors}%</p>
          </div>
        </div>

        {/* Logs Section (Solves Issue #16) */}
        <div className="logs-section">
          <h2>Recent Activity Logs</h2>
          <table className="logs-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Method</th>
                <th>Endpoint</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log, index) => (
                <tr key={index}>
                  <td>{log.time}</td>
                  <td><span className={`badge ${log.method}`}>{log.method}</span></td>
                  <td>{log.url}</td>
                  <td>
                    <span className={log.status === 200 ? "status-ok" : "status-err"}>
                      {log.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

export default App;