import React, { useState, useEffect, useCallback } from 'react';
import { apisAPI } from '../utils/api';
import { toast } from 'react-toastify';
import { Plus, Edit2, Trash2, Eye } from 'lucide-react';
import APIModal from './APIModal';
import APIDetailsModal from './APIDetailsModal';

const Dashboard = () => {
  const [apis, setApis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedApi, setSelectedApi] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalItems, setTotalItems] = useState(0);

  const pageSize = 10;

  const fetchApis = useCallback(async () => {
    setLoading(true);
    try {
      const response = await apisAPI.getAll(page, pageSize);
      setApis(response.data.apis);
      setTotalPages(response.data.pages);
      setTotalItems(
        response.data.total ||
        response.data.count ||
        0
      );
    } catch (error) {
      toast.error('Failed to fetch APIs');
    } finally {
      setLoading(false);
    }
  }, [page, pageSize]);

  useEffect(() => {
    fetchApis();
  }, [fetchApis]);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  const startItem = (page - 1) * pageSize + 1;
  const endItem = Math.min(page * pageSize, totalItems);

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <h1>My APIs</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={18} /> Create API
        </button>
      </div>

      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Method</th>
              <th>Endpoint</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {apis.map((api) => (
              <tr key={api._id}>
                <td>{api.name}</td>
                <td>{api.method}</td>
                <td style={{ maxWidth: '300px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {api.endpoint}
                </td>
                <td>{api.status}</td>
                <td>
                  <Eye onClick={() => { setSelectedApi(api); setShowDetailsModal(true); }} />
                  <Edit2 onClick={() => { setSelectedApi(api); setShowModal(true); }} />
                  <Trash2 onClick={() => apisAPI.delete(api._id).then(fetchApis)} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px', flexWrap: 'wrap' }}>
          <div>Showing {startItem}-{endItem} of {totalItems} items</div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button onClick={() => setPage(1)} disabled={page === 1}>First</button>
            <button onClick={() => setPage(page - 1)} disabled={page === 1}>Prev</button>
            <span>Page {page} of {totalPages}</span>
            <button onClick={() => setPage(page + 1)} disabled={page === totalPages}>Next</button>
            <button onClick={() => setPage(totalPages)} disabled={page === totalPages}>Last</button>
          </div>
        </div>
      )}

      {showModal && <APIModal api={selectedApi} onClose={() => { setShowModal(false); fetchApis(); }} />}
      {showDetailsModal && <APIDetailsModal api={selectedApi} onClose={() => setShowDetailsModal(false)} />}
    </div>
  );
};

export default Dashboard;
