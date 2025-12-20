import React, { useState, useEffect } from 'react';
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

  const fetchApis = async () => {
    setLoading(true);
    try {
      const response = await apisAPI.getAll(page, 10);
      setApis(response.data.apis);
      setTotalPages(response.data.pages);
    } catch (error) {
      toast.error('Failed to fetch APIs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApis();
  }, [page]);

  const handleCreate = () => {
    setSelectedApi(null);
    setShowModal(true);
  };

  const handleEdit = (api) => {
    setSelectedApi(api);
    setShowModal(true);
  };

  const handleView = (api) => {
    setSelectedApi(api);
    setShowDetailsModal(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this API?')) {
      try {
        await apisAPI.delete(id);
        toast.success('API deleted successfully');
        fetchApis();
      } catch (error) {
        toast.error('Failed to delete API');
      }
    }
  };

  const handleModalClose = (refresh) => {
    setShowModal(false);
    setSelectedApi(null);
    if (refresh) {
      fetchApis();
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>My APIs</h1>
        <button className="btn btn-primary" onClick={handleCreate}>
          <Plus size={18} style={{ marginRight: '5px' }} />
          Create API
        </button>
      </div>

      {apis.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
          <p>No APIs found. Create your first API to get started!</p>
        </div>
      ) : (
        <>
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
                    <td>
                      <span className={`badge badge-${api.method === 'GET' ? 'info' : api.method === 'POST' ? 'success' : 'warning'}`}>
                        {api.method}
                      </span>
                    </td>
                    <td style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {api.endpoint}
                    </td>
                    <td>
                      <span className={`badge badge-${api.status === 'active' ? 'success' : 'danger'}`}>
                        {api.status}
                      </span>
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '10px' }}>
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '5px 10px' }}
                          onClick={() => handleView(api)}
                        >
                          <Eye size={16} />
                        </button>
                        <button
                          className="btn btn-primary"
                          style={{ padding: '5px 10px' }}
                          onClick={() => handleEdit(api)}
                        >
                          <Edit2 size={16} />
                        </button>
                        <button
                          className="btn btn-danger"
                          style={{ padding: '5px 10px' }}
                          onClick={() => handleDelete(api._id)}
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

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

      {showModal && (
        <APIModal
          api={selectedApi}
          onClose={handleModalClose}
        />
      )}

      {showDetailsModal && (
        <APIDetailsModal
          api={selectedApi}
          onClose={() => setShowDetailsModal(false)}
        />
      )}
    </div>
  );
};

export default Dashboard;