import React, { useState, useEffect } from 'react';
import { keysAPI } from '../utils/api';
import { toast } from 'react-toastify';
import { Plus, Trash2, Copy, Power } from 'lucide-react';

const APIKeys = () => {
  const [keys, setKeys] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [keyName, setKeyName] = useState('');

  const fetchKeys = async () => {
    setLoading(true);
    try {
      const response = await keysAPI.getAll();
      setKeys(response.data.keys);
    } catch (error) {
      toast.error('Failed to fetch API keys');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchKeys();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await keysAPI.create({ name: keyName });
      toast.success('API key created successfully');
      setShowModal(false);
      setKeyName('');
      fetchKeys();
    } catch (error) {
      toast.error('Failed to create API key');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this API key?')) {
      try {
        await keysAPI.delete(id);
        toast.success('API key deleted successfully');
        fetchKeys();
      } catch (error) {
        toast.error('Failed to delete API key');
      }
    }
  };

  const handleToggle = async (id) => {
    try {
      await keysAPI.toggle(id);
      toast.success('API key status updated');
      fetchKeys();
    } catch (error) {
      toast.error('Failed to update API key');
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('API key copied to clipboard');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>API Keys</h1>
        <button className="btn btn-primary" onClick={() => setShowModal(true)}>
          <Plus size={18} style={{ marginRight: '5px' }} />
          Create API Key
        </button>
      </div>

      {keys.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
          <p>No API keys found. Create your first API key to get started!</p>
        </div>
      ) : (
        <div className="card">
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Key</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {keys.map((key) => (
                <tr key={key._id}>
                  <td>{key.name}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <code style={{ 
                        background: '#f5f5f5', 
                        padding: '5px 10px', 
                        borderRadius: '4px',
                        fontSize: '12px'
                      }}>
                        {key.key.substring(0, 20)}...
                      </code>
                      <button
                        className="btn btn-secondary"
                        style={{ padding: '5px 10px' }}
                        onClick={() => copyToClipboard(key.key)}
                      >
                        <Copy size={16} />
                      </button>
                    </div>
                  </td>
                  <td>
                    <span className={`badge badge-${key.is_active ? 'success' : 'danger'}`}>
                      {key.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>{new Date(key.created_at).toLocaleDateString()}</td>
                  <td>
                    <div style={{ display: 'flex', gap: '10px' }}>
                      <button
                        className="btn btn-secondary"
                        style={{ padding: '5px 10px' }}
                        onClick={() => handleToggle(key._id)}
                      >
                        <Power size={16} />
                      </button>
                      <button
                        className="btn btn-danger"
                        style={{ padding: '5px 10px' }}
                        onClick={() => handleDelete(key._id)}
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
      )}

      {showModal && (
        <div className="modal" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Create API Key</h2>
              <button className="close-btn" onClick={() => setShowModal(false)}>×</button>
            </div>
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label>Key Name</label>
                <input
                  type="text"
                  className="form-control"
                  value={keyName}
                  onChange={(e) => setKeyName(e.target.value)}
                  placeholder="e.g., Production Key"
                  required
                />
              </div>
              <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
                <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                  Create
                </button>
                <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)} style={{ flex: 1 }}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default APIKeys;
