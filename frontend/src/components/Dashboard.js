import React, { useState, useEffect } from 'react';
import { apisAPI } from '../utils/api';
import { toast } from 'react-toastify';
import {
  Search, Filter, SortAsc, SortDesc, Plus,
  Trash2, Edit2, Eye
} from 'lucide-react';
import APIModal from './APIModal';
import APIDetailsModal from './APIDetailsModal';

const Dashboard = () => {
  const [apis, setApis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [methodFilter, setMethodFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const [showModal, setShowModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedApi, setSelectedApi] = useState(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchApis();
    }, 300);
    return () => clearTimeout(timer);
  }, [search, methodFilter, statusFilter, sortBy, sortOrder, page]);

  const fetchApis = async () => {
    setLoading(true);
    try {
      const response = await apisAPI.getAll(page, 10, search, methodFilter, statusFilter, sortBy, sortOrder);
      setApis(response.data.apis);
      setTotalPages(response.data.pages);
    } catch (error) {
      console.error(error);
      toast.error('Failed to fetch APIs');
    } finally {
      setLoading(false);
    }
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

  const handleEdit = (api) => {
    setSelectedApi(api);
    setShowModal(true);
  };

  const handleView = (api) => {
    setSelectedApi(api);
    setShowDetailsModal(true);
  };

  const handleModalClose = () => {
    setShowModal(false);
    setShowDetailsModal(false);
    setSelectedApi(null);
    fetchApis();
  };

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>My APIs</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={18} style={{ marginRight: '8px' }} />
          Create New API
        </button>
      </div>

      {/* Search and Filter Controls */}
      <div className="card" style={{ marginBottom: '20px', padding: '20px' }}>
        <div style={{ display: 'flex', gap: '15px', alignItems: 'center', flexWrap: 'wrap' }}>
          {/* Search Input */}
          <div style={{ display: 'flex', alignItems: 'center', minWidth: '250px' }}>
            <Search size={18} style={{ marginRight: '8px', color: '#666' }} />
            <input
              type="text"
              placeholder="Search APIs by name or endpoint..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{
                padding: '8px 12px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                flex: 1,
                fontSize: '14px'
              }}
            />
          </div>

          {/* Method Filter */}
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <Filter size={18} style={{ marginRight: '8px', color: '#666' }} />
            <select
              value={methodFilter}
              onChange={(e) => setMethodFilter(e.target.value)}
              style={{
                padding: '8px 12px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                minWidth: '100px',
                fontSize: '14px'
              }}
            >
              <option value="">All Methods</option>
              <option value="GET">GET</option>
              <option value="POST">POST</option>
              <option value="PUT">PUT</option>
              <option value="DELETE">DELETE</option>
              <option value="PATCH">PATCH</option>
            </select>
          </div>

          {/* Status Filter */}
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              style={{
                padding: '8px 12px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                minWidth: '100px',
                fontSize: '14px'
              }}
            >
              <option value="">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>

          {/* Sort Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '14px', color: '#666' }}>Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              style={{
                padding: '8px 12px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '14px'
              }}
            >
              <option value="created_at">Created Date</option>
              <option value="updated_at">Updated Date</option>
              <option value="name">Name</option>
            </select>
            <button
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              style={{
                padding: '8px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                background: 'white',
                cursor: 'pointer'
              }}
              title={sortOrder === 'asc' ? 'Ascending' : 'Descending'}
            >
              {sortOrder === 'asc' ? <SortAsc size={16} /> : <SortDesc size={16} />}
            </button>
          </div>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>Loading...</div>
      ) : apis.length === 0 ? (
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
