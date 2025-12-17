import React, { useState, useEffect } from 'react';
import { logsAPI } from '../utils/api';
import { toast } from 'react-toastify';
import { Activity, CheckCircle, XCircle, Clock } from 'lucide-react';

const Analytics = () => {
  const [stats, setStats] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [statsResponse, logsResponse] = await Promise.all([
        logsAPI.getStats(),
        logsAPI.getAll(page, 20)
      ]);
      setStats(statsResponse.data);
      setLogs(logsResponse.data.logs);
      setTotalPages(logsResponse.data.pages);
    } catch (error) {
      toast.error('Failed to fetch analytics data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [page]);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <h1 style={{ marginBottom: '20px' }}>Analytics</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Requests</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Activity size={32} color="#007bff" />
            <div className="value">{stats.total_requests}</div>
          </div>
        </div>

        <div className="stat-card">
          <h3>Success Requests</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <CheckCircle size={32} color="#28a745" />
            <div className="value">{stats.success_requests}</div>
          </div>
        </div>

        <div className="stat-card">
          <h3>Error Requests</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <XCircle size={32} color="#dc3545" />
            <div className="value">{stats.error_requests}</div>
          </div>
        </div>

        <div className="stat-card">
          <h3>Avg Response Time</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Clock size={32} color="#ffc107" />
            <div className="value">{stats.avg_response_time}ms</div>
          </div>
        </div>
      </div>

      <div className="card">
        <h2 style={{ marginBottom: '20px' }}>Recent Requests</h2>
        {logs.length === 0 ? (
          <p>No logs found</p>
        ) : (
          <>
            <table className="table">
              <thead>
                <tr>
                  <th>Method</th>
                  <th>Endpoint</th>
                  <th>Status</th>
                  <th>Response Time</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log._id}>
                    <td>
                      <span className={`badge badge-${log.method === 'GET' ? 'info' : log.method === 'POST' ? 'success' : 'warning'}`}>
                        {log.method}
                      </span>
                    </td>
                    <td style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {log.endpoint}
                    </td>
                    <td>
                      <span className={`badge badge-${log.status_code >= 200 && log.status_code < 300 ? 'success' : 'danger'}`}>
                        {log.status_code}
                      </span>
                    </td>
                    <td>{log.response_time ? `${log.response_time.toFixed(2)}ms` : 'N/A'}</td>
                    <td>{new Date(log.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            {totalPages > 1 && (
              <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginTop: '20px' }}>
                <button
                  className="btn btn-secondary"
                  onClick={() => setPage(page - 1)}
                  disabled={page === 1}
                >
                  Previous
                </button>
                <span style={{ padding: '10px' }}>Page {page} of {totalPages}</span>
                <button
                  className="btn btn-secondary"
                  onClick={() => setPage(page + 1)}
                  disabled={page === totalPages}
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Analytics;
