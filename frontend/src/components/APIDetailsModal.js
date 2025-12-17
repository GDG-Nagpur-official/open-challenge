import React from 'react';
import { X } from 'lucide-react';

const APIDetailsModal = ({ api, onClose }) => {
  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>API Details</h2>
          <button className="close-btn" onClick={onClose}>
            <X size={24} />
          </button>
        </div>
        <div>
          <div style={{ marginBottom: '15px' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Name:</strong>
            <p style={{ color: 'var(--text-primary)' }}>{api.name}</p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Description:</strong>
            <p style={{ color: 'var(--text-primary)' }}>{api.description || 'No description'}</p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Endpoint:</strong>
            <p style={{ wordBreak: 'break-all', color: 'var(--text-primary)' }}>{api.endpoint}</p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Method:</strong>
            <p>
              <span className={`badge badge-${api.method === 'GET' ? 'info' : api.method === 'POST' ? 'success' : 'warning'}`}>
                {api.method}
              </span>
            </p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Status:</strong>
            <p>
              <span className={`badge badge-${api.status === 'active' ? 'success' : 'danger'}`}>
                {api.status}
              </span>
            </p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Created:</strong>
            <p style={{ color: 'var(--text-primary)' }}>{new Date(api.created_at).toLocaleString()}</p>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Last Updated:</strong>
            <p style={{ color: 'var(--text-primary)' }}>{new Date(api.updated_at).toLocaleString()}</p>
          </div>
          <button className="btn btn-secondary" onClick={onClose} style={{ width: '100%' }}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default APIDetailsModal;
